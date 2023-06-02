use std::{error::Error, time::Duration};

use tokio::time::interval;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let mut interval = interval(Duration::from_secs(60));
    loop {
        interval.tick().await;
        println!("Hello, world!");
    }
}
