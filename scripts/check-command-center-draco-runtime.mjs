import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const root = process.cwd();
const glbPath = path.join(root, "public", "world", "art", "command-center.glb");
const decoderPath = path.join(root, "public", "draco", "draco_decoder.js");
const artPath = path.join(root, "src", "world", "art", "CommandCenterArt.tsx");
const headersPath = path.join(root, "public", "_headers");

const EXPECTED_GLB_SHA256 = "72008b693cf0fc889aea7cf8af94ec2876cc0e3a7807b430e6e483fe275d7496";
const EXPECTED_GLB_BYTES = 845512;
const failures = [];

function readGlbJson(file) {
  const data = fs.readFileSync(file);
  if (data.length < 20) throw new Error("GLB too small");
  const magic = data.readUInt32LE(0);
  const version = data.readUInt32LE(4);
  const declared = data.readUInt32LE(8);
  const jsonLength = data.readUInt32LE(12);
  const jsonType = data.readUInt32LE(16);
  if (magic !== 0x46546c67) throw new Error("invalid GLB magic");
  if (version !== 2) throw new Error(`unexpected GLB version ${version}`);
  if (declared !== data.length) throw new Error("declared GLB length mismatch");
  if (jsonType !== 0x4e4f534a) throw new Error("first GLB chunk is not JSON");
  return {
    data,
    json: JSON.parse(data.subarray(20, 20 + jsonLength).toString("utf8").trim()),
  };
}

if (!fs.existsSync(glbPath)) failures.push("missing command-center.glb");
if (!fs.existsSync(decoderPath)) failures.push("missing self-hosted public/draco/draco_decoder.js");
if (!fs.existsSync(artPath)) failures.push("missing CommandCenterArt.tsx");
if (!fs.existsSync(headersPath)) failures.push("missing public/_headers");

if (!failures.length) {
  const { data, json } = readGlbJson(glbPath);
  const sha = crypto.createHash("sha256").update(data).digest("hex");
  if (data.length !== EXPECTED_GLB_BYTES) failures.push(`GLB byte size changed: ${data.length}`);
  if (sha !== EXPECTED_GLB_SHA256) failures.push(`GLB SHA-256 changed: ${sha}`);

  const used = new Set(json.extensionsUsed ?? []);
  const required = new Set(json.extensionsRequired ?? []);
  if (!used.has("KHR_draco_mesh_compression") || !required.has("KHR_draco_mesh_compression")) {
    failures.push("certified Command Center GLB is no longer the expected Draco-compressed asset");
  }

  const source = fs.readFileSync(artPath, "utf8");
  const requiredSnippets = [
    "DRACOLoader",
    "setDecoderPath",
    "/draco/",
    "setDecoderConfig",
    "type: \"js\"",
  ];
  for (const snippet of requiredSnippets) {
    if (!source.includes(snippet)) failures.push(`CommandCenterArt.tsx missing ${snippet}`);
  }
  if (!/useGLTF\(\s*COMMAND_CENTER_ART_ASSET\s*,\s*false\s*,/.test(source)) {
    failures.push("CommandCenterArt must disable Drei's default Draco loader");
  }

  const decoder = fs.readFileSync(decoderPath);
  if (decoder.length < 100000) failures.push("self-hosted Draco JS decoder is implausibly small");
  const decoderText = decoder.toString("utf8", 0, Math.min(decoder.length, 20000));
  if (!decoderText.includes("DracoDecoderModule")) {
    failures.push("self-hosted decoder does not look like the Draco JavaScript decoder");
  }

  const headers = fs.readFileSync(headersPath, "utf8");
  if (headers.includes("wasm-unsafe-eval") || headers.includes("unsafe-eval")) {
    failures.push("CSP was weakened with eval/WebAssembly execution permission");
  }
  if (/gstatic\.com|googleapis\.com/.test(headers)) {
    failures.push("CSP was widened for an external Draco CDN");
  }
}

if (failures.length) {
  console.error("COMMAND CENTER DRACO RUNTIME: FAIL");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log("COMMAND CENTER DRACO RUNTIME: PASS");
console.log(`glb_sha256=${EXPECTED_GLB_SHA256}`);
console.log(`glb_bytes=${EXPECTED_GLB_BYTES}`);
console.log("decoder=self-hosted-js");
console.log("csp=unchanged-no-wasm-eval");
