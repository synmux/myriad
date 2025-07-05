# frozen_string_literal: true

require 'fileutils'
require 'pathname'
require_relative 'utils'

module Dimensions
  # Types of file operations
  module OperationType
    MOVE = 'move'
    COPY = 'copy'
    SYMLINK = 'symlink'

    def self.valid?(operation)
      [MOVE, COPY, SYMLINK].include?(operation)
    end

    def self.all
      [MOVE, COPY, SYMLINK]
    end
  end

  # Organizes image files by dimensions using move, copy, or symlink operations
  class FileOrganizer
    include Utils

    attr_reader :success_count, :failure_count, :failed_operations

    def initialize(logger)
      @logger = logger
      @success_count = 0
      @failure_count = 0
      @failed_operations = []
    end

    # Organize files by dimensions into subdirectories
    def organize_files(results, target_directory, operation, dry_run = false)
      target_dir = Pathname.new(target_directory)

      @logger.info("Starting file organization - operation: #{operation}, " \
                   "target: #{target_directory}, dry_run: #{dry_run}, " \
                   "dimensions: #{results.length}")

      if dry_run
        preview_operations(results, target_dir, operation)
      else
        execute_operations(results, target_dir, operation)
      end

      @logger.info("File organization completed - success: #{@success_count}, " \
                   "failure: #{@failure_count}")
    end

    # Get organization statistics
    def statistics
      {
        'success_count' => @success_count,
        'failure_count' => @failure_count,
        'total_operations' => @success_count + @failure_count
      }
    end

    # Reset success and failure counters
    def reset_counters
      @success_count = 0
      @failure_count = 0
      @failed_operations.clear
    end

    # Check if target directory is writable
    def self.check_target_directory_writable(target_dir)
      dir = Pathname.new(target_dir)

      begin
        dir.mkpath unless dir.exist?

        # Test write permissions by creating a temporary file
        test_file = dir / '.dimensions_write_test'
        test_file.write('')
        test_file.delete
        true
      rescue StandardError
        false
      end
    end

    private

    # Preview operations without executing them
    def preview_operations(results, target_directory, operation)
      @logger.info('[DRY RUN] Previewing file operations')

      total_files = 0
      results.each do |dimension_str, stats|
        safe_dim = safe_filename(dimension_str)
        dimension_dir = target_directory / safe_dim

        total_files += stats.files.length

        @logger.info("[DRY RUN] Would create directory: #{dimension_dir}")
        @logger.info("[DRY RUN] Would #{operation} #{stats.files.length} files to #{dimension_dir}")

        # Show sample files
        stats.files.first(3).each do |file_path|
          source = Pathname.new(file_path)
          target = dimension_dir / source.basename
          @logger.info("[DRY RUN] #{source} -> #{target}")
        end

        @logger.info("[DRY RUN] ... and #{stats.files.length - 3} more files") if stats.files.length > 3
      end

      @logger.info("[DRY RUN] Total files to #{operation}: #{total_files}")
    end

    # Execute file operations
    def execute_operations(results, target_directory, operation)
      reset_counters

      # Ensure target directory exists
      begin
        ensure_directory(target_directory)
      rescue IOError => e
        @logger.error("Cannot create target directory: #{e.message}")
        return
      end

      results.each do |dimension_str, stats|
        safe_dim = safe_filename(dimension_str)
        dimension_dir = target_directory / safe_dim

        # Create dimension subdirectory
        begin
          ensure_directory(dimension_dir)
          @logger.info("Created dimension directory: #{dimension_dir}")
        rescue IOError => e
          @logger.error("Cannot create dimension directory: #{dimension_dir} - #{e.message}")
          @failure_count += stats.files.length
          next
        end

        # Process files in this dimension
        stats.files.each do |file_path|
          process_single_file(Pathname.new(file_path), dimension_dir, operation)
        end
      end
    end

    # Process a single file operation
    def process_single_file(source_path, target_dir, operation)
      target_path = target_dir / source_path.basename

      # Handle filename conflicts
      target_path = resolve_filename_conflict(target_path) if target_path.exist?

      begin
        case operation
        when OperationType::MOVE
          FileUtils.mv(source_path.to_s, target_path.to_s)
        when OperationType::COPY
          FileUtils.cp(source_path.to_s, target_path.to_s, preserve: true)
        when OperationType::SYMLINK
          # Try relative symlink first
          begin
            relative_source = source_path.realpath.relative_path_from(target_path.parent.realpath)
            target_path.make_symlink(relative_source.to_s)
          rescue ArgumentError
            # Use absolute path if relative doesn't work
            target_path.make_symlink(source_path.realpath.to_s)
          end
        end

        @success_count += 1
        @logger.debug("Successfully #{operation}d file: #{source_path} -> #{target_path}")
      rescue StandardError => e
        @failure_count += 1
        error_info = {
          'source' => source_path.to_s,
          'target' => target_path.to_s,
          'operation' => operation,
          'error' => e.message
        }
        @failed_operations << error_info
        @logger.warn("Failed to #{operation} file: #{source_path} -> #{target_path} - #{e.message}")
      end
    end

    # Resolve filename conflicts by adding a suffix
    def resolve_filename_conflict(target_path)
      base_name = target_path.basename(target_path.extname).to_s
      extension = target_path.extname
      parent = target_path.parent

      counter = 1
      loop do
        new_name = "#{base_name}_#{counter}#{extension}"
        new_path = parent / new_name
        return new_path unless new_path.exist?

        counter += 1
      end
    end
  end
end
