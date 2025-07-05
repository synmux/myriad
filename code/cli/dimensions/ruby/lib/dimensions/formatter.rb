# frozen_string_literal: true

require 'json'
require 'psych'
require 'tty-table'
require 'pastel'
require_relative 'utils'

module Dimensions
  # Formats and outputs dimension analysis results
  class OutputFormatter
    include Utils

    def initialize(logger)
      @logger = logger
      @pastel = Pastel.new
    end

    # Format and output results in the specified format
    def format_results(results:, format_type: 'text', sort_by: 'count', 
                      min_count: 1, max_results: nil, output_file: nil)
      # Filter and sort results
      filtered_results = filter_and_sort_results(results, sort_by, min_count, max_results)
      
      # Generate summary statistics
      summary = generate_summary(results, filtered_results)

      # Format based on type
      case format_type
      when 'text'
        output_text_format(filtered_results, summary, output_file)
      when 'json'
        output_json_format(filtered_results, summary, output_file)
      when 'yaml'
        output_yaml_format(filtered_results, summary, output_file)
      else
        raise ArgumentError, "Unsupported format type: #{format_type}"
      end
    end

    # Show processing summary to stderr
    def show_progress_summary(total_processed:, total_failed:, processing_time:)
      $stderr.puts "\n#{@pastel.green('Processing completed!')}"
      $stderr.puts "  Processed: #{total_processed.to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')} images"
      if total_failed.positive?
        $stderr.puts "  #{@pastel.yellow("Failed: #{total_failed.to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')} images")}"
      end
      $stderr.puts "  Time: #{'%.2f' % processing_time} seconds"
      if total_processed.positive?
        rate = total_processed / processing_time
        $stderr.puts "  Rate: #{'%.1f' % rate} images/second"
      end
      $stderr.puts
    end

    private

    # Filter and sort dimension statistics
    def filter_and_sort_results(results, sort_by, min_count, max_results)
      # Filter by minimum count
      filtered = results.values.select { |stats| stats.count >= min_count }

      # Sort based on criteria
      case sort_by
      when 'count'
        filtered.sort_by! { |x| -x.count }
      when 'dimensions'
        filtered.sort_by! { |x| [x.width, x.height] }
      else
        raise ArgumentError, "Unsupported sort criteria: #{sort_by}"
      end

      # Limit results
      filtered = filtered.first(max_results) if max_results

      filtered
    end

    # Generate summary statistics
    def generate_summary(all_results, filtered_results)
      total_images = all_results.values.sum(&:count)
      total_size = all_results.values.sum(&:total_size)
      unique_dimensions = all_results.length

      # Find most common dimension
      most_common = all_results.values.max_by(&:count)

      {
        'total_images' => total_images,
        'unique_dimensions' => unique_dimensions,
        'total_size_bytes' => total_size,
        'total_size' => format_file_size(total_size),
        'most_common_dimension' => most_common&.dimensions_str || 'None',
        'most_common_count' => most_common&.count || 0,
        'displayed_results' => filtered_results.length
      }
    end

    # Calculate percentage with zero division protection
    def calculate_percentage(count, total)
      return 0.0 if total.zero?
      (count.to_f / total) * 100
    end

    # Output results in rich text format
    def output_text_format(results, summary, output_file)
      output = if output_file
                 File.open(output_file, 'w')
               else
                 $stdout
               end

      # Summary table
      summary_table = TTY::Table.new(
        header: ['Metric', 'Value'],
        rows: [
          ['Total Images', summary['total_images'].to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')],
          ['Unique Dimensions', summary['unique_dimensions'].to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')],
          ['Total Size', summary['total_size']],
          ['Most Common', "#{summary['most_common_dimension']} (#{summary['most_common_count'].to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')} images)"]
        ]
      )

      output.puts @pastel.bold("Summary Statistics")
      output.puts summary_table.render(:unicode, padding: [0, 1])
      output.puts

      # Results table
      if results.any?
        print_results(summary, results, output)
      else
        output.puts @pastel.yellow("No results match the specified criteria.")
      end

      output.close if output_file
    end

    # Print results table
    def print_results(summary, results, output)
      rows = results.map do |stats|
        percentage = calculate_percentage(stats.count, summary['total_images'])
        sample_files = truncate_file_list(stats.files, 3)

        [
          stats.dimensions_str,
          stats.count.to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,'),
          "#{'%.1f' % percentage}%",
          stats.formatted_size,
          sample_files
        ]
      end

      results_table = TTY::Table.new(
        header: ['Dimensions', 'Count', 'Percentage', 'Total Size', 'Sample Files'],
        rows: rows
      )

      title = "Image Dimensions Analysis - #{summary['total_images'].to_s.gsub(/(\d)(?=(\d{3})+(?!\d))/, '\\1,')} images"
      output.puts @pastel.bold(title)
      output.puts results_table.render(:unicode, padding: [0, 1])
    end

    # Build dimension data structure
    def build_dimension_data(results, summary, include_all_files: false)
      results.map do |stats|
        percentage = calculate_percentage(stats.count, summary['total_images'])

        dimension_entry = {
          'width' => stats.width,
          'height' => stats.height,
          'dimensions' => stats.dimensions_str,
          'count' => stats.count,
          'percentage' => percentage.round(1),
          'total_size_bytes' => stats.total_size,
          'total_size' => stats.formatted_size
        }

        if include_all_files
          dimension_entry['files'] = stats.files
        else
          dimension_entry['sample_files'] = stats.files.first(5)
        end

        dimension_entry
      end
    end

    # Output results in JSON format
    def output_json_format(results, summary, output_file)
      dimensions_data = build_dimension_data(results, summary, include_all_files: true)
      output_data = {
        'summary' => summary,
        'dimensions' => dimensions_data
      }

      json_str = JSON.pretty_generate(output_data)

      if output_file
        File.write(output_file, json_str)
      else
        puts json_str
      end
    end

    # Output results in YAML format
    def output_yaml_format(results, summary, output_file)
      dimensions_data = build_dimension_data(results, summary, include_all_files: true)
      output_data = {
        'summary' => summary,
        'dimensions' => dimensions_data
      }

      yaml_str = Psych.dump(output_data)

      if output_file
        File.write(output_file, yaml_str)
      else
        puts yaml_str
      end
    end
  end
end