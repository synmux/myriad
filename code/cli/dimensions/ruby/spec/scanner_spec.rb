# frozen_string_literal: true

require 'spec_helper'
require 'tmpdir'
require 'fileutils'

RSpec.describe Dimensions::DirectoryScanner do
  let(:logger) { Logger.new(File::NULL) }
  let(:scanner) { described_class.new(logger) }

  describe '#scan_directory' do
    it 'raises error for non-existent directory' do
      expect { scanner.scan_directory('/non/existent/path') }.to raise_error(Errno::ENOENT)
    end

    it 'raises error for non-directory path' do
      Dir.mktmpdir do |tmpdir|
        file_path = File.join(tmpdir, 'test.txt')
        File.write(file_path, 'test')

        expect { scanner.scan_directory(file_path) }.to raise_error(ArgumentError)
      end
    end

    it 'finds image files in directory' do
      Dir.mktmpdir do |tmpdir|
        # Create test image files
        image_files = ['test1.jpg', 'test2.png', 'test3.gif']
        image_files.each do |filename|
          File.write(File.join(tmpdir, filename), 'fake image data')
        end

        # Create non-image files
        File.write(File.join(tmpdir, 'test.txt'), 'text file')

        result = scanner.scan_directory(tmpdir)

        expect(result.length).to eq(3)
        expect(result.map(&:basename).map(&:to_s).sort).to eq(image_files.sort)
      end
    end

    it 'scans recursively' do
      Dir.mktmpdir do |tmpdir|
        # Create nested directory structure
        subdir = File.join(tmpdir, 'subdir')
        FileUtils.mkdir_p(subdir)

        File.write(File.join(tmpdir, 'root.jpg'), 'image')
        File.write(File.join(subdir, 'nested.png'), 'image')

        result = scanner.scan_directory(tmpdir)

        expect(result.length).to eq(2)
        expect(result.map(&:basename).map(&:to_s).sort).to eq(['nested.png', 'root.jpg'])
      end
    end

    it 'skips hidden directories' do
      Dir.mktmpdir do |tmpdir|
        # Create hidden directory
        hidden_dir = File.join(tmpdir, '.hidden')
        FileUtils.mkdir_p(hidden_dir)

        File.write(File.join(tmpdir, 'visible.jpg'), 'image')
        File.write(File.join(hidden_dir, 'hidden.png'), 'image')

        result = scanner.scan_directory(tmpdir)

        expect(result.length).to eq(1)
        expect(result.first.basename.to_s).to eq('visible.jpg')
      end
    end
  end

  describe '#reset_counters' do
    it 'clears failed and skipped files' do
      scanner.instance_variable_set(:@failed_files, ['file1'])
      scanner.instance_variable_set(:@skipped_files, ['file2'])

      scanner.reset_counters

      expect(scanner.failed_files).to be_empty
      expect(scanner.skipped_files).to be_empty
    end
  end
end
