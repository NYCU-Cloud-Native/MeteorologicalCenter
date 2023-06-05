use std::{env, error::Error, time::Duration};

use axum::{routing::get, Router};
use controller::task::run_task;
use tokio::time::interval;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    dotenvy::dotenv().unwrap();
    let mut endpoints = Vec::new();
    for (key, value) in env::vars() {
        if key.ends_with("_CRAWLER_ENDPOINT") {
            endpoints.push(value);
        }
    }
    let endpoints_bak = endpoints.clone();
    tokio::spawn(async move {
        let mut interval = interval(Duration::from_secs(60));
        loop {
            interval.tick().await;
            if let Err(e) = run_task(&endpoints_bak).await {
                eprintln!("run periodic task failed: {}", e);
            }
        }
    });
    let app = Router::new().route(
        "/update",
        get(|| async move {
            if let Err(e) = run_task(&endpoints).await {
                eprintln!("run periodic task failed: {}", e);
            }
        }),
    );
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
    Ok(())
}
