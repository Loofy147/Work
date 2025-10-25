import { render, screen } from '@testing-library/react';
import App from './App';

test('renders generate and analyze button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/generate and analyze/i);
  expect(buttonElement).toBeInTheDocument();
});
