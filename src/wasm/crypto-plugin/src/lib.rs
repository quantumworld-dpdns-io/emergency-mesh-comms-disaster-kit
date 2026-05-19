#[unsafe(no_mangle)]
pub extern "C" fn verify_crc32(expected: u32, actual: u32) -> i32 {
    if expected == actual { 1 } else { 0 }
}
