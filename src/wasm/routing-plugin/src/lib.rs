#[unsafe(no_mangle)]
pub extern "C" fn should_forward(priority: i32, lqi: i32) -> i32 {
    if priority >= 2 {
        return 1;
    }
    if lqi >= 55 {
        return 1;
    }
    0
}
