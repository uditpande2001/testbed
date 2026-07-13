import fs from "node:fs/promises";
import path from "node:path";
import {
  Presentation,
  PresentationFile,
} from "file:///C:/Users/cenau/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const OUT = "D:/testbed/project_ppt_reviewed.pptx";
const MEDIA = "D:/testbed/tmp_review/media";
const PREVIEW = "D:/testbed/tmp_review/reviewed_preview";

async function imageBytes(fileName) {
  const bytes = await fs.readFile(path.join(MEDIA, fileName));
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function addRule(slide) {
  slide.shapes.add({
    geometry: "rect",
    position: { left: 80, top: 56, width: 1040, height: 3 },
    fill: "#111827",
    line: { style: "solid", fill: "none", width: 0 },
  });
  slide.shapes.add({
    geometry: "rect",
    position: { left: 80, top: 642, width: 1040, height: 2 },
    fill: "#9ca3af",
    line: { style: "solid", fill: "none", width: 0 },
  });
}

function addSlideNumber(slide, number) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position: { left: 1128, top: 630, width: 48, height: 28 },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = String(number);
  box.text.style = { fontSize: 14, color: "#374151", alignment: "right" };
}

function addTitle(slide, title) {
  const titleBox = slide.shapes.add({
    geometry: "textbox",
    position: { left: 80, top: 86, width: 960, height: 58 },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  titleBox.text = title.toUpperCase();
  titleBox.text.style = { fontSize: 28, color: "#111827" };
}

function addBody(slide, text, position, fontSize = 22) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = { fontSize, color: "#111827" };
  return box;
}

function addAccentBox(slide, title, body, left, top, width, height, color) {
  slide.shapes.add({
    geometry: "roundRect",
    position: { left, top, width, height },
    fill: "#f9fafb",
    line: { style: "solid", fill: color, width: 2 },
    borderRadius: "rounded-lg",
  });
  addBody(slide, title, { left: left + 18, top: top + 16, width: width - 36, height: 34 }, 18)
    .text.style = { fontSize: 18, color, bold: true };
  addBody(slide, body, { left: left + 18, top: top + 56, width: width - 36, height: height - 72 }, 16);
}

function technicalSlide(presentation, title, number) {
  const slide = presentation.slides.add();
  slide.background.fill = "#ffffff";
  addRule(slide);
  addTitle(slide, title);
  addSlideNumber(slide, number);
  return slide;
}

async function main() {
  await fs.mkdir(PREVIEW, { recursive: true });

  const presentation = Presentation.create({
    slideSize: { width: 1280, height: 720 },
  });

  // 1. Title
  {
    const slide = presentation.slides.add();
    slide.background.fill = "#06152f";
    slide.images.add({
      blob: await imageBytes("image1.jpeg"),
      contentType: "image/jpeg",
      alt: "Smart meter and metadata knowledge graph title visual",
      fit: "contain",
      position: { left: 0, top: 0, width: 1280, height: 720 },
    });
  }

  // 2. Problem
  {
    const slide = technicalSlide(presentation, "Why metadata lineage matters", 1);
    addBody(
      slide,
      "Enterprise data lakes can store large volumes of data, but the context around those datasets is scattered.",
      { left: 90, top: 162, width: 980, height: 70 },
      24,
    );
    addAccentBox(
      slide,
      "Fragmented metadata",
      "Schemas, storage paths, topics, and pipeline context are hard to inspect in one place.",
      90,
      270,
      310,
      190,
      "#1d4ed8",
    );
    addAccentBox(
      slide,
      "Relationship complexity",
      "Traditional tables are awkward for dynamic relationships between datasets, processes, runs, and columns.",
      455,
      270,
      330,
      190,
      "#047857",
    );
    addAccentBox(
      slide,
      "Lineage blindspot",
      "Without run-level evidence, it is difficult to prove when a schema changed and which run caused it.",
      840,
      270,
      330,
      190,
      "#b45309",
    );
  }

  // 3. Objective
  {
    const slide = technicalSlide(presentation, "The testbed turns pipeline activity into a queryable graph", 2);
    addBody(
      slide,
      "Project objective",
      { left: 90, top: 164, width: 360, height: 40 },
      26,
    ).text.style = { fontSize: 26, color: "#111827", bold: true };
    addBody(
      slide,
      "Automatically extract dataset schemas from lakehouse files, model them as RDF knowledge graph entities, and use OpenLineage/Marquez to trace runs and schema changes.",
      { left: 90, top: 214, width: 1040, height: 98 },
      22,
    );
    addAccentBox(slide, "Metadata extraction", "Read Parquet files from MinIO and extract columns, data types, row counts, and null counts.", 90, 360, 320, 160, "#1d4ed8");
    addAccentBox(slide, "Knowledge graph", "Map datasets, columns, storage systems, and metadata collections into RDF and load them into GraphDB.", 480, 360, 320, 160, "#047857");
    addAccentBox(slide, "Lineage evidence", "Capture OpenLineage events in Marquez and export compact SchemaChange nodes into GraphDB.", 870, 360, 320, 160, "#b45309");
  }

  // 4. Architecture
  {
    const slide = technicalSlide(presentation, "End-to-end architecture", 3);
    slide.images.add({
      blob: await imageBytes("image2.png"),
      contentType: "image/png",
      alt: "Metadata knowledge graph architecture diagram",
      fit: "contain",
      position: { left: 58, top: 124, width: 1164, height: 480 },
    });
  }

  // 5. Metadata processing
  {
    const slide = technicalSlide(presentation, "Metadata processing creates the dataset view", 4);
    addAccentBox(slide, "1. Discover datasets", "List Parquet objects in MinIO for meter-data and command-response.", 100, 178, 300, 168, "#1d4ed8");
    addAccentBox(slide, "2. Extract schema", "Read columns, data types, row counts, null counts, and storage paths.", 490, 178, 300, 168, "#047857");
    addAccentBox(slide, "3. Generate RDF", "Create RDF triples using the ontology and serialize dataset TTL files.", 880, 178, 300, 168, "#7c3aed");
    addAccentBox(slide, "4. Load GraphDB", "Clear stale triples and reload the current metadata and lineage graph.", 295, 406, 300, 168, "#b45309");
    addAccentBox(slide, "5. Query columns", "Use SPARQL to inspect datasets, columns, data types, and lineage changes.", 685, 406, 300, 168, "#be123c");
  }

  // 6. Lineage tracking
  {
    const slide = technicalSlide(presentation, "Lineage tracking records the run that changed a schema", 5);
    addBody(
      slide,
      "The consumer writes Parquet through the lakehouse writer. That writer emits an OpenLineage event with the output schema. Marquez stores the run history, and the lineage pipeline exports compact schema-change evidence to GraphDB.",
      { left: 90, top: 150, width: 1040, height: 104 },
      21,
    );
    slide.images.add({
      blob: await imageBytes("image3.jpeg"),
      contentType: "image/jpeg",
      alt: "Marquez dataset job dataset lineage visual",
      fit: "contain",
      position: { left: 100, top: 302, width: 640, height: 100 },
    });
    addAccentBox(slide, "GraphDB lineage nodes", "DataCollectionRun\nSchemaVersion\nSchemaChange\naddsColumn / removesColumn / changesColumn", 790, 282, 330, 190, "#1d4ed8");
  }

  // 7. Demo plan
  {
    const slide = technicalSlide(presentation, "Demo proves schema-change lineage with real consumer output", 6);
    addAccentBox(slide, "Baseline", "Run the real Kafka consumers.\nThey write the original meter-data and command-response schemas.", 88, 214, 300, 190, "#1d4ed8");
    addAccentBox(slide, "Changed run", "Run demo.run_changed_schema.\nIt preserves the latest real rows and adds campus context columns.", 490, 214, 300, 190, "#047857");
    addAccentBox(slide, "Evidence", "Run main.py and query GraphDB.\nThe graph returns the run ID that added each column.", 892, 214, 300, 190, "#b45309");
    addBody(slide, "Added demo columns: run_location, department, building, demo_run_label, operator_group", { left: 145, top: 488, width: 990, height: 46 }, 22)
      .text.style = { fontSize: 22, color: "#111827", bold: true, alignment: "center" };
  }

  // 8. Result
  {
    const slide = technicalSlide(presentation, "GraphDB identifies which run added each column", 7);
    const headers = ["Process", "Run", "Added column"];
    const rows = [
      ["meter-data-pipeline", "OpenLineage run ID", "run_location"],
      ["meter-data-pipeline", "OpenLineage run ID", "department"],
      ["meter-data-pipeline", "OpenLineage run ID", "building"],
      ["command-response-pipeline", "OpenLineage run ID", "operator_group"],
    ];
    const left = 110;
    const top = 174;
    const widths = [360, 350, 300];
    const rowH = 58;
    for (let c = 0; c < 3; c++) {
      slide.shapes.add({
        geometry: "rect",
        position: { left: left + widths.slice(0, c).reduce((a, b) => a + b, 0), top, width: widths[c], height: rowH },
        fill: "#111827",
        line: { style: "solid", fill: "#ffffff", width: 1 },
      });
      addBody(slide, headers[c], { left: left + widths.slice(0, c).reduce((a, b) => a + b, 0) + 14, top: top + 15, width: widths[c] - 28, height: 34 }, 18)
        .text.style = { fontSize: 18, color: "#ffffff", bold: true };
    }
    rows.forEach((row, r) => {
      for (let c = 0; c < 3; c++) {
        const x = left + widths.slice(0, c).reduce((a, b) => a + b, 0);
        slide.shapes.add({
          geometry: "rect",
          position: { left: x, top: top + rowH * (r + 1), width: widths[c], height: rowH },
          fill: r % 2 === 0 ? "#f9fafb" : "#eef2ff",
          line: { style: "solid", fill: "#d1d5db", width: 1 },
        });
        addBody(slide, row[c], { left: x + 14, top: top + rowH * (r + 1) + 14, width: widths[c] - 28, height: 34 }, 17);
      }
    });
    addBody(
      slide,
      "SPARQL pattern: SchemaChange -> observedInRun -> DataCollectionRun -> runId",
      { left: 145, top: 565, width: 990, height: 42 },
      20,
    ).text.style = { fontSize: 20, color: "#374151", alignment: "center" };
  }

  // 9. Demo transition
  {
    const slide = technicalSlide(presentation, "Now let us move onto the demonstration", 8);
    addBody(
      slide,
      "We will run the real consumers, add controlled schema changes, reload GraphDB, and query the run that introduced each new column.",
      { left: 180, top: 260, width: 920, height: 120 },
      30,
    ).text.style = { fontSize: 30, color: "#111827", alignment: "center" };
  }

  // 10. Close
  {
    const slide = technicalSlide(presentation, "What the testbed demonstrates", 9);
    addBody(
      slide,
      "The system turns raw pipeline activity into queryable metadata knowledge.",
      { left: 120, top: 178, width: 1040, height: 64 },
      28,
    ).text.style = { fontSize: 28, color: "#111827", bold: true, alignment: "center" };
    addAccentBox(slide, "Datasets", "What datasets exist and where they are stored.", 110, 310, 240, 150, "#1d4ed8");
    addAccentBox(slide, "Columns", "What columns they contain and their data types.", 390, 310, 240, 150, "#047857");
    addAccentBox(slide, "Processes", "Which jobs consume and create datasets.", 670, 310, 240, 150, "#7c3aed");
    addAccentBox(slide, "Runs", "Which run introduced a schema change.", 950, 310, 240, 150, "#b45309");
    addBody(slide, "Thank you", { left: 470, top: 540, width: 340, height: 60 }, 32)
      .text.style = { fontSize: 32, color: "#111827", bold: true, alignment: "center" };
  }

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    const png = await presentation.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(PREVIEW, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  }
  const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
  await fs.writeFile(path.join(PREVIEW, "montage.webp"), new Uint8Array(await montage.arrayBuffer()));

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(OUT);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});


