const withImages = require('next-images');
const withSass = require('@zeit/next-sass');
const withCss = require('@zeit/next-css');
const withPlugins = require('next-compose-plugins');

// load .env variables
require('dotenv').config();

const nextConfig = {
  env: {
    API_URL: process.env.API_URL,
  },
};

module.exports = withPlugins(
  [
    [
      withSass,
      {
        cssModules: true,
        sassLoaderOptions: {
          includePaths: ['styles'],
        },
      },
    ],
    [
      withCss,
      {
        cssModules: false,
      }
    ],
    [withImages],
  ],
  nextConfig
);
