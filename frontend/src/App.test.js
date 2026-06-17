import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, it, expect, vi } from 'vitest';
import App from './App';

// Mock child components to focus on App logic
vi.mock('./components/Background', () => ({
    default: () => <div data-testid="background" />
}));

vi.mock('./views/HomeView', () => ({
    default: () => <div data-testid="home-view">书灵 BookSage</div>
}));

vi.mock('./views/ResultsView', () => ({
    default: () => <div data-testid="results-view" />
}));

vi.mock('./components/Footer', () => ({
    default: () => <footer data-testid="footer" />
}));

vi.mock('./components/BookCard', () => ({
    default: ({ book }) => <div data-testid="book-card">{book.title}</div>
}));

describe('App', () => {
    beforeEach(() => {
        global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve([]) }));
    });

    it('renders basic structure', async () => {
        render(<App />);

        expect(screen.getByTestId('background')).toBeInTheDocument();
        expect(screen.getByTestId('home-view')).toBeInTheDocument();
        expect(screen.getByTestId('footer')).toBeInTheDocument();
        await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/popular'));
    });
});
