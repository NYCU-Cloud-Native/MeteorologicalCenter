use std::{env, error::Error, time::Duration};

use axum::{routing::get, Router};
use controller::task::run_task;
use tokio::time::interval;

fn extract_endpoints_from_envs<T: Iterator<Item = (String, String)>>(envs: T) -> Vec<String> {
    let mut endpoints = Vec::new();
    for (key, value) in envs {
        if key.ends_with("_CRAWLER_ENDPOINT") {
            endpoints.push(value);
        }
    }
    endpoints
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    dotenvy::dotenv().unwrap();
    let endpoints = extract_endpoints_from_envs(env::vars());
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn extract_endpoints_from_envs_with_empty_envs_should_not_contains_any_endpoint() {
        let envs: Vec<(String, String)> = vec![];
        let endpoints = extract_endpoints_from_envs(envs.into_iter());
        assert_eq!(endpoints.len(), 0);
    }

    #[test]
    fn extract_endpoints_from_envs_with_a_valid_crawler_endpoint_should_return_endpoint() {
        let envs: Vec<(String, String)> = vec![(
            "TEST_CRAWLER_ENDPOINT".into(),
            "http://example.com:5000".into(),
        )];
        let endpoints = extract_endpoints_from_envs(envs.into_iter());
        assert_eq!(endpoints[0], "http://example.com:5000");
    }

    #[test]
    fn extract_endpoints_from_envs_with_two_valid_crawler_endpoints_should_return_two_endpoints() {
        let envs: Vec<(String, String)> = vec![
            (
                "TEST_CRAWLER_ENDPOINT".into(),
                "http://example.com:5000".into(),
            ),
            (
                "ANOTHER_TEST_CRAWLER_ENDPOINT".into(),
                "http://example2.com:5000".into(),
            ),
        ];
        let endpoints = extract_endpoints_from_envs(envs.into_iter());
        assert!(endpoints.contains(&String::from("http://example.com:5000")));
        assert!(endpoints.contains(&String::from("http://example2.com:5000")));
    }

    #[test]
    fn extract_endpoints_from_envs_with_not_valid_endpoint_should_contains_any_endpoint() {
        let envs: Vec<(String, String)> = vec![("TEST".into(), "http://example.com:5000".into())];
        let endpoints = extract_endpoints_from_envs(envs.into_iter());
        assert_eq!(endpoints.len(), 0);
    }
}
