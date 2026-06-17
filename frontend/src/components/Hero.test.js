import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import Hero from './Hero';

describe('Hero', () => {
    beforeEach(() => {
        global.fetch = vi.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve([]),
            })
        );
    });

    it('renders hero title and search items', () => {
        render(<Hero />);

        expect(screen.getByText(/书灵 BookSage/i)).toBeInTheDocument();
        expect(screen.getByPlaceholderText(/搜索一本你喜欢的书/i)).toBeInTheDocument();
    });

    it('updates input value on change', async () => {
        render(<Hero />);
        const input = screen.getByPlaceholderText(/搜索一本你喜欢的书/i);

        fireEvent.change(input, { target: { value: 'Harry Potter' } });
        expect(input.value).toBe('Harry Potter');
        await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/search_books?query=Harry%20Potter'));
    });

    it('calls onRecommend when a method button is clicked', async () => {
        const onRecommend = vi.fn();
        render(<Hero onRecommend={onRecommend} />);

        const input = screen.getByPlaceholderText(/搜索一本你喜欢的书/i);
        fireEvent.change(input, { target: { value: 'Harry Potter' } });
        await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/search_books?query=Harry%20Potter'));

        fireEvent.click(screen.getByRole('button', { name: /显示推荐方式/i }));
        const hybridButton = screen.getByRole('button', { name: /混合推荐/i });
        fireEvent.click(hybridButton);

        expect(onRecommend).toHaveBeenCalledWith('Harry Potter', 'hybrid');
    });
});
