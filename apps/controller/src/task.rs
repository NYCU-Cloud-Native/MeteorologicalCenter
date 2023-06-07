use crate::crawler::{crawler_client::CrawlerClient, Request};
use std::error::Error;

pub async fn run_task(endpoints: &Vec<String>) -> Result<(), Box<dyn Error + Send + Sync>> {
    for endpoint in endpoints {
        let mut client = CrawlerClient::connect(endpoint.clone()).await?;
        let request = tonic::Request::new(Request {});
        match client.run(request).await {
            Ok(_) => println!("triggered {}", endpoint),
            Err(e) => eprintln!("trigger {} failed: {}", endpoint, e),
        }
    }
    println!("task runned");
    Ok(())
}
