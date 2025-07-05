# frozen_string_literal: true

require 'mini_magick'
require 'parallel'
require 'pathname'
require_relative 'utils'

module Dimensions
  # Information about a single image file
  ImageInfo = Struct.new(:path, :width, :height, :file_size, :dimensions_str) do
    def initialize(path:, width:, height:, file_size:, dimensions_str: nil)
      super(path, width, height, file_size, dimensions_str || "#{width}×#{height}")
    end
  end

  # Statistics for a specific dimension
  DimensionStats = Struct.new(:width, :height, :count, :total_size, :files) do
    include Utils

    def dimensions_str
      "#{width}×#{height}"
    end

    def formatted_size
      format_file_size(total_size)
    end
  end

  # Processes image files to extract dimension information
  class ImageProcessor
    include Utils

    attr_reader :failed_files, :processed_files

    def initialize(logger)
      @logger = logger
      @failed_files = []
      @processed_files = []
      @dimension_cache = {}
      @mutex = Mutex.new
    end

    # Process multiple image files to extract dimensions
    def process_images(image_paths, max_workers = 1, &progress_callback)
      @logger.info("Starting image processing - total: #{image_paths.length}, workers: #{max_workers}")

      if max_workers == 1
        # Single-threaded processing
        image_paths.each do |path|
          process_single_image(path)
          progress_callback&.call(1)
        end
      else
        # Multi-threaded processing using Parallel gem
        Parallel.each(image_paths, in_threads: max_workers) do |path|
          process_single_image(path)
          progress_callback&.call(1)
        end
      end

      # Aggregate results
      results = aggregate_results

      @logger.info("Image processing completed - processed: #{@processed_files.length}, " \
                   "failed: #{@failed_files.length}, unique dimensions: #{results.length}")

      results
    end

    # Clear the dimension cache
    def clear_cache
      @dimension_cache.clear
    end

    # Reset failed and processed file lists
    def reset_counters
      @failed_files.clear
      @processed_files.clear
    end

    private

    # Process a single image file to extract dimensions
    def process_single_image(image_path)
      path_str = image_path.to_s

      # Check cache first
      if @dimension_cache.key?(path_str)
        width, height = @dimension_cache[path_str]
        file_size = get_file_size(image_path)
        create_and_store_image_info(path_str, width, height, file_size)
        return
      end

      # Process the image
      begin
        image = MiniMagick::Image.open(path_str)
        width = image.width
        height = image.height
        file_size = get_file_size(image_path)

        # Cache the result
        @mutex.synchronize do
          @dimension_cache[path_str] = [width, height]
        end

        create_and_store_image_info(path_str, width, height, file_size)

      rescue StandardError => e
        @logger.warn("Failed to process image: #{path_str} - #{e.message}")
        @mutex.synchronize do
          @failed_files << path_str
        end
      end
    end

    # Create ImageInfo object and store it in processed files list
    def create_and_store_image_info(path_str, width, height, file_size)
      info = ImageInfo.new(
        path: path_str,
        width: width,
        height: height,
        file_size: file_size
      )
      
      @mutex.synchronize do
        @processed_files << info
      end
      
      info
    end

    # Aggregate processed image results by dimensions
    def aggregate_results
      dimension_map = {}

      @processed_files.each do |info|
        dim_str = info.dimensions_str

        dimension_map[dim_str] ||= DimensionStats.new(
          info.width,
          info.height,
          0,
          0,
          []
        )

        stats = dimension_map[dim_str]
        stats.count += 1
        stats.total_size += info.file_size
        stats.files << info.path
      end

      dimension_map
    end
  end
end