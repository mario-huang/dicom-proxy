import {
  findScu,
  findScuOptions,
  moveScu,
  moveScuOptions,
} from "dicom-dimse-native";

const options: findScuOptions = {
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
  tags: [
    {
      key: "00080052",
      value: "STUDY",
    },
    {
      key: "00100010",
      value: "",
    },
  ],
  verbose: true,
};

findScu(options, (result) => {
  console.log(JSON.parse(result));
});

const moveOptions: moveScuOptions = {
  source: {
    aet: "MY_AET",
    ip: "127.0.0.1",
    port: 9999,
  },
  target: {
    aet: "TARGET_AET",
    ip: "127.0.0.1",
    port: 5678,
  },
  tags: [
    {
      key: "0020000D",
      value: "1.3.46.670589.5.2.10.2156913941.892665384.993397",
    },
    {
      key: "00080052",
      value: "STUDY",
    },
  ],
  destination: "MY_AET", // e.g. sending to ourself
  verbose: true,
};
moveScu(moveOptions, (result) => {
  console.log(JSON.parse(result));
});
