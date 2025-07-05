# frozen_string_literal: true

require 'spec_helper'

RSpec.describe Dimensions::Utils do
  describe '.format_file_size' do
    it 'formats bytes correctly' do
      expect(described_class.format_file_size(0)).to eq('0 B')
      expect(described_class.format_file_size(512)).to eq('512 B')
      expect(described_class.format_file_size(1024)).to eq('1.0 KB')
      expect(described_class.format_file_size(1_048_576)).to eq('1.0 MB')
      expect(described_class.format_file_size(1_073_741_824)).to eq('1.0 GB')
    end
  end

  describe '.image_file?' do
    it 'recognizes image file extensions' do
      expect(described_class.image_file?('test.jpg')).to be true
      expect(described_class.image_file?('test.png')).to be true
      expect(described_class.image_file?('test.gif')).to be true
      expect(described_class.image_file?('test.heic')).to be true
      expect(described_class.image_file?('test.txt')).to be false
      expect(described_class.image_file?('test')).to be false
    end

    it 'handles case insensitive extensions' do
      expect(described_class.image_file?('test.JPG')).to be true
      expect(described_class.image_file?('test.PNG')).to be true
    end
  end

  describe '.truncate_file_list' do
    it 'handles empty lists' do
      expect(described_class.truncate_file_list([])).to eq('No files')
    end

    it 'shows all files when under limit' do
      files = ['/path/to/file1.jpg', '/path/to/file2.png']
      expect(described_class.truncate_file_list(files)).to eq('file1.jpg, file2.png')
    end

    it 'truncates when over limit' do
      files = ['/path/to/file1.jpg', '/path/to/file2.png', '/path/to/file3.gif', '/path/to/file4.bmp']
      result = described_class.truncate_file_list(files, 3)
      expect(result).to eq('file1.jpg, file2.png, file3.gif (+1)')
    end
  end

  describe '.safe_filename' do
    it 'makes safe filenames' do
      expect(described_class.safe_filename('1920×1080')).to eq('1920x1080')
      expect(described_class.safe_filename('1920:1080')).to eq('1920-1080')
      expect(described_class.safe_filename('1920/1080')).to eq('1920-1080')
    end
  end
end