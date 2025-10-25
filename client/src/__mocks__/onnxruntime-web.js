// client/src/__mocks__/onnxruntime-web.js

class MockInferenceSession {
  static async create(path) {
    // Simulate async model loading
    await new Promise(resolve => setTimeout(resolve, 100));
    return new MockInferenceSession();
  }

  async run(feeds) {
    // Return a dummy prediction
    const output = new Float32Array(10); // 10 vertices
    return { output: { data: output } };
  }
}

export const InferenceSession = MockInferenceSession;
export const Tensor = jest.fn();
