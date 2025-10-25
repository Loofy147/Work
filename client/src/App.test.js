import { render, screen } from '@testing-library/react';
import App from './App';

test('renders generate model button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/generate model/i);
  expect(buttonElement).toBeInTheDocument();
});
