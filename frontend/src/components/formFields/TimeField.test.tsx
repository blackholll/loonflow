import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TimeField from '../components/formFields/TimeField';
import DateField from '../components/formFields/DateField';

// 测试 TimeField 组件
describe('TimeField', () => {
    const defaultProps = {
        fieldRequired: false,
        onChange: jest.fn(),
        mode: 'edit' as const,
        props: {}
    };

    test('renders time input field', () => {
        render(<TimeField value="" {...defaultProps} />);
        const timeInput = screen.getByRole('textbox');
        expect(timeInput).toBeInTheDocument();
    });

    test('displays time value correctly', () => {
        const testValue = '2023-12-01T14:30:00.000Z';
        render(<TimeField value={testValue} {...defaultProps} />);
        const timeInput = screen.getByRole('textbox') as HTMLInputElement;
        expect(timeInput.value).toBe('14:30');
    });

    test('calls onChange when time changes', () => {
        const onChange = jest.fn();
        render(<TimeField value="" {...defaultProps} onChange={onChange} />);
        const timeInput = screen.getByRole('textbox');
        fireEvent.change(timeInput, { target: { value: '15:45' } });
        expect(onChange).toHaveBeenCalled();
    });

    test('supports HH:mm:ss format', () => {
        const propsWithSeconds = {
            ...defaultProps,
            props: { format: 'HH:mm:ss' }
        };
        render(<TimeField value="2023-12-01T14:30:45.000Z" {...propsWithSeconds} />);
        const timeInput = screen.getByRole('textbox') as HTMLInputElement;
        expect(timeInput.value).toBe('14:30:45');
    });

    test('renders in view mode', () => {
        render(<TimeField value="2023-12-01T14:30:00.000Z" {...defaultProps} mode="view" />);
        // 在 view 模式下应该显示格式化的时间文本
        expect(screen.getByText(/14:30/)).toBeInTheDocument();
    });
});

// 测试 DateField 组件
describe('DateField', () => {
    const defaultProps = {
        fieldRequired: false,
        onChange: jest.fn(),
        mode: 'edit' as const,
        props: {}
    };

    test('renders date input field', () => {
        render(<DateField value="" {...defaultProps} />);
        const dateInput = screen.getByRole('textbox');
        expect(dateInput).toBeInTheDocument();
    });

    test('displays date value correctly', () => {
        const testValue = '2023-12-01T00:00:00.000Z';
        render(<DateField value={testValue} {...defaultProps} />);
        const dateInput = screen.getByRole('textbox') as HTMLInputElement;
        expect(dateInput.value).toBe('2023-12-01');
    });

    test('calls onChange when date changes', () => {
        const onChange = jest.fn();
        render(<DateField value="" {...defaultProps} onChange={onChange} />);
        const dateInput = screen.getByRole('textbox');
        fireEvent.change(dateInput, { target: { value: '2023-12-25' } });
        expect(onChange).toHaveBeenCalled();
    });

    test('supports YYYY-MM-DD HH:mm format', () => {
        const propsWithTime = {
            ...defaultProps,
            props: { format: 'YYYY-MM-DD HH:mm' }
        };
        render(<DateField value="2023-12-01T14:30:00.000Z" {...propsWithTime} />);
        const dateInput = screen.getByRole('textbox') as HTMLInputElement;
        expect(dateInput.value).toBe('2023-12-01T14:30');
    });

    test('supports YYYY-MM-DD HH:mm:ss format', () => {
        const propsWithSeconds = {
            ...defaultProps,
            props: { format: 'YYYY-MM-DD HH:mm:ss' }
        };
        render(<DateField value="2023-12-01T14:30:45.000Z" {...propsWithSeconds} />);
        const dateInput = screen.getByRole('textbox') as HTMLInputElement;
        expect(dateInput.value).toBe('2023-12-01T14:30:45');
    });

    test('renders in view mode', () => {
        render(<DateField value="2023-12-01T14:30:00.000Z" {...defaultProps} mode="view" />);
        // 在 view 模式下应该显示格式化的日期文本
        expect(screen.getByText(/2023/)).toBeInTheDocument();
    });
});
