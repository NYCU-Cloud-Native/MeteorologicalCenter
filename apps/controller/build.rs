fn main() {
    tonic_build::configure()
        .compile(&["proto/crawler.proto"], &["proto"])
        .unwrap();
}
