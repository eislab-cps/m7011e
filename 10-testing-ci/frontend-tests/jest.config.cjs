module.exports = {
  rootDir: '.',
  testEnvironment: 'jsdom',
  modulePaths: ['<rootDir>/node_modules'],
  testMatch: ['<rootDir>/**/*.test.jsx'],
  collectCoverageFrom: ['src/TodoList.jsx'],
  coverageDirectory: '<rootDir>/coverage',
  transform: {
    '^.+\\.[jt]sx?$': ['babel-jest', {
      presets: [
        ['@babel/preset-env', { targets: { node: 'current' } }],
        ['@babel/preset-react', { runtime: 'automatic' }],
      ],
    }],
  },
};
