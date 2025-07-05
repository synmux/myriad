# frozen_string_literal: true

require 'pathname'
require 'logger'

module Dimensions
  # Utility functions for the dimensions CLI tool
  module Utils
    SUPPORTED_EXTENSIONS = %w[
      .jpg .jpeg .png .gif .bmp .tiff .tif .webp
      .heic .heif .heics .heifs .hif .dng
    ].freeze

    module_function

    # Format file size in bytes to human-readable string
    def format_file_size(size_bytes)
      return '0 B' if size_bytes.zero?

      size_names = %w[B KB MB GB TB]
      size = size_bytes.to_f
      i = 0

      while size >= 1024.0 && i < size_names.length - 1
        size /= 1024.0
        i += 1
      end

      if i.zero?
        format('%d %s', size.to_i, size_names[i])
      else
        format('%.1f %s', size, size_names[i])
      end
    end

    # Check if a file is a supported image format
    def image_file?(file_path)
      return false unless file_path.is_a?(Pathname) || file_path.is_a?(String)

      path = Pathname.new(file_path)
      SUPPORTED_EXTENSIONS.include?(path.extname.downcase)
    end

    # Get file size in bytes, handling errors gracefully
    def get_file_size(file_path)
      Pathname.new(file_path).size
    rescue StandardError
      0
    end

    # Truncate a list of filenames for display
    def truncate_file_list(files, max_length = 3)
      return 'No files' if files.empty?

      filenames = files.map { |f| File.basename(f) }

      if filenames.length <= max_length
        filenames.join(', ')
      else
        displayed = filenames.first(max_length)
        remaining = filenames.length - max_length
        "#{displayed.join(', ')} (+#{remaining})"
      end
    end

    # Ensure a directory exists, creating it if necessary
    def ensure_directory(path)
      dir = Pathname.new(path)
      dir.mkpath unless dir.exist?
    rescue SystemCallError => e
      raise IOError, "Cannot create directory #{path}: #{e}"
    end

    # Create a safe filename from dimensions string
    def safe_filename(dimensions)
      dimensions.gsub('×', 'x').gsub(':', '-').gsub('/', '-')
    end

    # Set up logging
    def setup_logging(level = 'INFO')
      logger = Logger.new($stderr)
      logger.level = Logger.const_get(level.upcase)
      
      # Custom formatter for cleaner output
      logger.formatter = proc do |severity, datetime, _progname, msg|
        timestamp = datetime.strftime('%Y-%m-%d %H:%M:%S')
        if msg.is_a?(Hash)
          # Handle structured logging
          main_msg = msg.delete(:message) || msg.delete('message') || ''
          extra = msg.map { |k, v| "#{k}=#{v}" }.join(' ')
          "[#{timestamp}] #{severity}: #{main_msg} #{extra}\n"
        else
          "[#{timestamp}] #{severity}: #{msg}\n"
        end
      end
      
      logger
    end
  end
end