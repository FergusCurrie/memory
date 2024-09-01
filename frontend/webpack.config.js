const path = require('path');
const webpack = require('webpack');
const dotenv = require('dotenv');

dotenv.config();

module.exports = {
  entry: './src/index.js', // Change entry point to .tsx if using React or .ts for plain TypeScript
  //entry: './static/test_script.js',
  output: {
    path: path.resolve(__dirname, '../static/frontend'),
    filename: '[name].js',
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx|js|jsx)$/, // Update this to include .ts and .tsx
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react', // Include this line if you are using React
              '@babel/preset-typescript', // Add TypeScript preset
            ],
          },
        },
      },
      {
        test: /\.css$/, // New rule for CSS files
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  optimization: {
    minimize: true,
  },
  devServer: {
    hot: true,
  },
  plugins: [
    new webpack.ProvidePlugin({
      process: 'process/browser',
    }),
  ],
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'], // Add .ts and .tsx here
    fallback: {
      process: require.resolve('process/browser'),
    },
    // fallback: {
    //   stream: require.resolve('stream-browserify'),
    //   crypto: require.resolve('crypto-browserify'),
    // },
  },
};
