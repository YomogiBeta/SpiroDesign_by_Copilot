const path = require("path");

module.exports = {
 mode: "production",
 entry: "./src/index.js",
 output: {
  filename: "zstd_webpacked.js",
  path: path.resolve(__dirname, "dist"),
  library: 'zstd_webpacked',
  libraryTarget: 'umd'
 },
 module: {
  rules: [
   {
    test: /zstd\.wasm/,
    type: "asset/resource",
   },
  ],
 },
};
