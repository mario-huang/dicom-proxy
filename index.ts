import {
  findScu,
  findScuOptions,
  moveScu,
  moveScuOptions,
  startStoreScp,
  storeScpOptions,
} from "dicom-dimse-native";
import config from "./config";

const options: findScuOptions = {
  source: config.source,
  target: config.target,
  verbose: config.verbose,
  tags: [
    {
      key: "00080052",
      value: "STUDY",
    },
    {
      key: "00100010",
      value: "",
    },
    {
      key: "00080061",
      value: "",
    },
  ],
};

// findScu(options, (result) => {
//   console.log(JSON.parse(result));
// });

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

const storeScpOptions: storeScpOptions = {
  source: config.source,
  peers: [],
  verbose: config.verbose,
  storagePath: config.storagePath,
  permissive: true,
};

startStoreScp(storeScpOptions, (result) => {
  console.log("startStoreScp");
  console.log(JSON.parse(result));
});
