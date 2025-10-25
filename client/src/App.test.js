import { render, screen, waitFor } from '@testing-library/react';
import App from './App';

jest.mock('onnxruntime-web');

test('renders generate and analyze button', async () => {
  render(<App />);

  // Wait for the mock session to "load" and the button to be enabled
  await waitFor(() => {
    const buttonElement = screen.getByText(/generate and analyze/i);
    expect(buttonElement).toBeInTheDocument();
  });
});
