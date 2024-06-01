import { init, compress, decompress } from "@bokuweb/zstd-wasm";

/**
 *
 * @param {Buffer} raw_data
 * @returns {Buffer}
 */
export const zstd_compress = async (raw_data) => {
 await init();
 return buffer.Buffer.from(compress(raw_data));
}

/**
 *
 * @param {Buffer} compressed_data
 * @returns {Buffer}
 */
export const zstd_decompress = async (compressed_data) => {
 await init();
 return buffer.Buffer.from(decompress(compressed_data));
}
