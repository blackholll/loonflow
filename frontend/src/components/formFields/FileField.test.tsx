import { render, screen, fireEvent } from '@testing-library/react';
import FileField from './FileField';

// Mock URL.createObjectURL and URL.revokeObjectURL
global.URL.createObjectURL = jest.fn(() => 'mock-url');
global.URL.revokeObjectURL = jest.fn();

// Mock File constructor
global.File = class MockFile {
    name: string;
    size: number;
    type: string;

    constructor(name: string, size: number, type: string) {
        this.name = name;
        this.size = size;
        this.type = type;
    }
} as any;

describe('FileField', () => {
    const defaultProps = {
        fieldRequired: false,
        onChange: jest.fn(),
        mode: 'edit' as const,
        props: {}
    };

    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('renders file upload area', () => {
        render(<FileField value="" {...defaultProps} />);
        expect(screen.getByText('点击选择文件或拖拽文件到此处')).toBeInTheDocument();
    });

    test('displays file list correctly', () => {
        const testFiles = [
            { id: '1', name: 'test1.pdf', size: 1024, type: 'application/pdf' },
            { id: '2', name: 'test2.jpg', size: 2048, type: 'image/jpeg' }
        ];
        render(<FileField value={testFiles} {...defaultProps} />);

        expect(screen.getByText('test1.pdf')).toBeInTheDocument();
        expect(screen.getByText('test2.jpg')).toBeInTheDocument();
        expect(screen.getByText('已选择的文件 (2)')).toBeInTheDocument();
    });

    test('handles file selection', () => {
        const onChange = jest.fn();
        render(<FileField value="" {...defaultProps} onChange={onChange} />);

        const fileInput = screen.getByRole('textbox', { hidden: true });
        const file = new File(['test content'], 'test.txt', { type: 'text/plain' });

        fireEvent.change(fileInput, { target: { files: [file] } });

        expect(onChange).toHaveBeenCalled();
    });

    test('displays file size correctly', () => {
        const testFiles = [
            { id: '1', name: 'test.pdf', size: 1024, type: 'application/pdf' }
        ];
        render(<FileField value={testFiles} {...defaultProps} />);

        expect(screen.getByText('1 KB')).toBeInTheDocument();
    });

    test('handles file deletion', () => {
        const onChange = jest.fn();
        const testFiles = [
            { id: '1', name: 'test.pdf', size: 1024, type: 'application/pdf' }
        ];
        render(<FileField value={testFiles} {...defaultProps} onChange={onChange} />);

        const deleteButton = screen.getByTitle('删除');
        fireEvent.click(deleteButton);

        expect(onChange).toHaveBeenCalledWith([]);
    });

    test('renders in view mode', () => {
        const testFiles = [
            { id: '1', name: 'test.pdf', size: 1024, type: 'application/pdf' }
        ];
        render(<FileField value={testFiles} {...defaultProps} mode="view" />);

        expect(screen.getByText('test.pdf')).toBeInTheDocument();
        expect(screen.getByText('1 KB')).toBeInTheDocument();
        // 在 view 模式下不应该显示上传区域
        expect(screen.queryByText('点击选择文件或拖拽文件到此处')).not.toBeInTheDocument();
    });

    test('shows error for oversized files', () => {
        const propsWithSizeLimit = {
            ...defaultProps,
            props: { maxSize: 1000 } // 1KB limit
        };
        render(<FileField value="" {...propsWithSizeLimit} />);

        const fileInput = screen.getByRole('textbox', { hidden: true });
        const largeFile = new File(['test content'], 'large.txt', { type: 'text/plain' });
        // Mock file size
        Object.defineProperty(largeFile, 'size', { value: 2000 });

        fireEvent.change(fileInput, { target: { files: [largeFile] } });

        expect(screen.getByText(/文件.*超过大小限制/)).toBeInTheDocument();
    });

    test('shows error for too many files', () => {
        const propsWithFileLimit = {
            ...defaultProps,
            props: { maxFiles: 2 }
        };
        const existingFiles = [
            { id: '1', name: 'test1.pdf', size: 1024, type: 'application/pdf' },
            { id: '2', name: 'test2.pdf', size: 1024, type: 'application/pdf' }
        ];
        render(<FileField value={existingFiles} {...propsWithFileLimit} />);

        const fileInput = screen.getByRole('textbox', { hidden: true });
        const newFile = new File(['test content'], 'test3.txt', { type: 'text/plain' });

        fireEvent.change(fileInput, { target: { files: [newFile] } });

        expect(screen.getByText(/最多只能上传 2 个文件/)).toBeInTheDocument();
    });

    test('displays required field error', () => {
        render(<FileField value="" {...defaultProps} fieldRequired={true} />);

        expect(screen.getByText('此字段为必填项')).toBeInTheDocument();
    });

    test('parses JSON string value correctly', () => {
        const jsonValue = JSON.stringify([
            { id: '1', name: 'test.pdf', size: 1024, type: 'application/pdf' }
        ]);
        render(<FileField value={jsonValue} {...defaultProps} />);

        expect(screen.getByText('test.pdf')).toBeInTheDocument();
    });

    test('handles empty value gracefully', () => {
        render(<FileField value="" {...defaultProps} mode="view" />);

        expect(screen.getByText('-')).toBeInTheDocument();
    });
});
