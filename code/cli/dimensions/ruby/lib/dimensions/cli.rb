# frozen_string_literal: true

require 'commander'
require 'pathname'
require 'tty-progressbar'
require_relative 'version'
require_relative 'scanner'
require_relative 'processor'
require_relative 'formatter'
require_relative 'organizer'
require_relative 'utils'

module Dimensions
  # Command-line interface for the dimensions analysis tool
  class CLI
    include Commander::Methods
    include Utils

    def run
      program :name, 'dimensions'
      program :version, VERSION
      program :description, DESCRIPTION

      default_command :analyze

      command :analyze do |c|
        c.syntax = 'dimensions [PATHS...] [options]'
        c.summary = 'Analyze image dimensions in directories'
        c.description = 'Analyze image dimensions in directories. If no paths provided, uses current directory.'

        c.option '--format STRING', String, 'Output format (text, json, yaml) [default: text]'
        c.option '--sort STRING', String, 'Sort results by count or dimensions [default: count]'
        c.option '--min-count INTEGER', Integer, 'Only show dimensions with at least N images [default: 1]'
        c.option '--max-results INTEGER', Integer, 'Limit number of results shown'
        c.option '--threads INTEGER', Integer, 'Number of processing threads [default: 1]'
        c.option '--log-level STRING', String, 'Logging level (DEBUG, INFO, WARNING, ERROR) [default: INFO]'
        c.option '--output PATH', String, 'Save output to file'
        c.option '--no-progress', 'Disable progress bars'
        c.option '--move PATH', String, 'Move images to directories by dimensions'
        c.option '--copy PATH', String, 'Copy images to directories by dimensions'
        c.option '--symlink PATH', String, 'Create symlinks to images by dimensions'
        c.option '--dry-run', 'Preview operations without executing them'

        c.action do |args, options|
          options.default(
            format: 'text',
            sort: 'count',
            min_count: 1,
            threads: 1,
            log_level: 'INFO'
          )

          # Validate and process options
          paths = args.empty? ? [Dir.pwd] : args
          execute_analysis(paths, options)
        end
      end

      run!
    end

    private

    def execute_analysis(paths, options)
      # Validate inputs
      operation_type, target_directory = validate_file_operations(options)
      
      if options.threads < 1
        error_exit('Number of threads must be at least 1')
      end

      # Set up logging and components
      logger = setup_logging(options.log_level)
      scanner = DirectoryScanner.new(logger)
      processor = ImageProcessor.new(logger)
      formatter = OutputFormatter.new(logger)
      organizer = FileOrganizer.new(logger) if operation_type

      begin
        start_time = Time.now
        logger.info("Starting image dimension analysis - directories: #{paths.join(', ')}")

        # Phase 1: Scan for image files
        image_files = scan_for_images(scanner, paths, !options.no_progress)
        logger.info("Found image files: #{image_files.length}")

        # Phase 2: Process images
        results = process_images_with_progress(
          processor, image_files, options.threads, !options.no_progress
        )
        processing_time = Time.now - start_time

        # Phase 3: File operations (if requested)
        handle_file_operations(
          organizer, results, operation_type, target_directory, 
          options.dry_run, !options.no_progress, logger
        )

        # Phase 4: Output results
        formatter.format_results(
          results: results,
          format_type: options.format,
          sort_by: options.sort,
          min_count: options.min_count,
          max_results: options.max_results,
          output_file: options.output ? Pathname.new(options.output) : nil
        )

        # Show processing summary (only for text format or if writing to file)
        if options.format == 'text' || options.output
          formatter.show_progress_summary(
            total_processed: processor.processed_files.length,
            total_failed: processor.failed_files.length,
            processing_time: processing_time
          )
        end

        # Log final statistics
        logger.info("Analysis completed successfully - processed: #{processor.processed_files.length}, " \
                    "failed: #{processor.failed_files.length}, unique dimensions: #{results.length}, " \
                    "time: #{'%.2f' % processing_time}s")

      rescue Interrupt
        error_exit("\nOperation cancelled by user.")
      rescue StandardError => e
        logger.error("Unexpected error during processing: #{e.message}")
        error_exit("Error: #{e.message}")
      end
    end

    def validate_file_operations(options)
      file_operations = [options.move, options.copy, options.symlink].compact
      
      if file_operations.length > 1
        error_exit('Only one of --move, --copy, or --symlink can be specified')
      end

      # Determine operation type and target directory
      operation_type = nil
      target_directory = nil

      if options.move
        operation_type = OperationType::MOVE
        target_directory = options.move
      elsif options.copy
        operation_type = OperationType::COPY
        target_directory = options.copy
      elsif options.symlink
        operation_type = OperationType::SYMLINK
        target_directory = options.symlink
      end

      # Validate dry-run usage
      if options.dry_run && operation_type.nil?
        error_exit('--dry-run can only be used with --move, --copy, or --symlink')
      end

      # Validate target directory writability for non-dry-run operations
      if operation_type && !options.dry_run && 
         !FileOrganizer.check_target_directory_writable(target_directory)
        error_exit("Cannot write to target directory: #{target_directory}")
      end

      [operation_type, target_directory ? Pathname.new(target_directory) : nil]
    end

    def scan_for_images(scanner, paths, show_progress)
      if show_progress
        if paths.length == 1
          $stderr.puts 'Scanning for image files...'
        else
          $stderr.puts "Scanning #{paths.length} directories for image files..."
        end
      end

      image_files = []
      paths.each do |path|
        scanner.reset_counters
        image_files.concat(scanner.scan_directory(path))
      end

      if image_files.empty?
        $stderr.puts 'No image files found in the specified directories.'
        exit 0
      end

      image_files
    end

    def process_images_with_progress(processor, image_files, threads, show_progress)
      if show_progress
        $stderr.puts "Processing #{image_files.length} image files..."

        progress_bar = TTY::ProgressBar.new(
          'Processing images [:bar] :current/:total :percent :elapsed :rate/s',
          total: image_files.length,
          width: 30,
          complete: '█',
          incomplete: '░'
        )

        results = processor.process_images(image_files, threads) do |count|
          progress_bar.advance(count)
        end

        progress_bar.finish
      else
        results = processor.process_images(image_files, threads)
      end

      results
    end

    def handle_file_operations(organizer, results, operation_type, target_directory, 
                              dry_run, show_progress, logger)
      return unless operation_type && organizer

      if show_progress
        $stderr.puts "\n#{operation_type.capitalize}ing files by dimensions..."
      end

      organizer.organize_files(results, target_directory, operation_type, dry_run)

      # Show organization statistics
      stats = organizer.statistics
      if dry_run
        logger.info('Dry run completed - no files were actually moved/copied/linked')
      else
        logger.info("File organization statistics: #{stats}")
        
        if organizer.failed_operations.any?
          logger.warn("Some file operations failed: #{organizer.failed_operations.length}")
        end
      end
    end

    def error_exit(message)
      $stderr.puts message
      exit 1
    end
  end
end