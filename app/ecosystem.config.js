module.exports = {
  /**
   * Application configuration
   * Note: all environment variables are required.
   *
   */
  apps : [
    {
      name      : "file-ingest",
      script    : "/scanner/bin/file_ingest",
      interpreter: "python",
      env: {
        PROCESS_INTERVAL: 60,
        S3_BUCKET_NAME : process.argv[5],
        S3_KEY_PREFIX : process.argv[6],
        S3_ACCESS_KEY_ID : process.argv[7],
        S3_SECRET_ACCESS_KEY : process.argv[8],
        S3_REGION_NAME : "eu-west-2",
        CLAMAV_URL : process.argv[9],
        CLAMAV_PORT : process.argv[10],
        INPUT_DIR : process.argv[11],
        OUTPUT_DIR : process.argv[12],
        QUARANTINE_DIR : process.argv[13],
      }
    }
  ]
};
