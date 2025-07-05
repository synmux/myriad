# frozen_string_literal: true

require 'find'
require 'pathname'
require_relative 'utils'

module Dimensions
  # Scans directories for image files recursively
  class DirectoryScanner
    include Utils

    attr_reader :failed_files, :skipped_files

    def initialize(logger)
      @logger = logger
      @failed_files = []
      @skipped_files = []
    end

    # Scan directory recursively for image files
    def scan_directory(directory)
      dir_path = Pathname.new(directory)
      
      unless dir_path.exist?
        raise Errno::ENOENT, "Directory does not exist: #{directory}"
      end
      
      unless dir_path.directory?
        raise ArgumentError, "Path is not a directory: #{directory}"
      end

      @logger.info("Starting directory scan: #{directory}")
      
      image_files = []
      
      begin
        Find.find(directory) do |path|
          next if path == directory
          
          path_obj = Pathname.new(path)
          
          # Skip hidden directories and common system directories
          if path_obj.directory?
            basename = path_obj.basename.to_s
            if basename.start_with?('.') || %w[__pycache__ node_modules .git .svn .hg].include?(basename)
              Find.prune
            end
            next
          end
          
          # Process files
          begin
            if path_obj.file?
              if image_file?(path_obj)
                image_files << path_obj
              else
                @skipped_files << path
              end
            end
          rescue StandardError => e
            @logger.warn("Cannot access file/directory: #{path} - #{e.message}")
            @failed_files << path
          end
        end
      rescue Errno::EACCES => e
        @logger.error("Permission denied accessing directory: #{directory} - #{e.message}")
        raise
      end
      
      @logger.info("Directory scan completed - failed: #{@failed_files.length}, skipped: #{@skipped_files.length}")
      
      image_files
    end

    # Count total number of image files in directory (for progress calculation)
    def count_images(directory)
      scan_directory(directory).length
    rescue StandardError => e
      @logger.error("Error counting images in #{directory}: #{e.message}")
      0
    end

    # Reset failed and skipped file counters
    def reset_counters
      @failed_files.clear
      @skipped_files.clear
    end
  end
end