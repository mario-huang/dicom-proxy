export default {
  source: {
    aet: "DicomProxy",
    ip: "192.168.3.119",
    port: 4000,
  },
  target: {
    aet: "UpstreamPacs",
    ip: "192.168.3.100",
    port: 4242,
  },
  verbose: true,
  storagePath: "./data"
};
