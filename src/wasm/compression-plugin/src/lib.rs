#[unsafe(no_mangle)]
pub extern "C" fn passthrough_len(input_len: i32) -> i32 {
    input_len
}

#[unsafe(no_mangle)]
pub extern "C" fn compress_stub() -> i32 {
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn decompress_stub() -> i32 {
    1
}
