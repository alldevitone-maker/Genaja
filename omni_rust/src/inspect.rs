use serde::Serialize;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;

#[derive(Serialize)]
pub struct InspectionReport {
    pub declared_type: String,
    pub detected_type: String,
    pub risk_level: String,
    pub recommended_action: String,
    pub can_auto_convert: bool,
    pub preview_summary: String,
    pub encoding_status: String,
    pub container_type: String,
    pub notes: Vec<String>,
}

pub fn run_inspection(path: &str) -> io::Result<()> {
    let mut notes = Vec::new();
    let file_path = Path::new(path);
    
    if !file_path.exists() {
        let report = InspectionReport {
            declared_type: "unknown".into(),
            detected_type: "unknown".into(),
            risk_level: "high".into(),
            recommended_action: "proceed".into(),
            can_auto_convert: false,
            preview_summary: "".into(),
            encoding_status: "utf-8".into(),
            container_type: "flat".into(),
            notes: vec!["Arquivo não encontrado no sistema operacional.".to_string()],
        };
        let json = serde_json::to_string(&report)?;
        println!("{}", json);
        return Ok(());
    }

    let ext = file_path.extension()
        .and_then(|e| e.to_str())
        .unwrap_or("unknown")
        .to_lowercase();
        
    let mut f = File::open(file_path)?;
    let mut buffer = [0; 2048];
    let bytes_read = f.read(&mut buffer)?;
    let header_bytes = &buffer[..bytes_read];
    
    let mut detected_type = "unknown".to_string();
    let mut container_type = "flat".to_string();
    let mut risk_level = "low".to_string();
    let mut recommended_action = "proceed".to_string();
    let mut can_auto_convert = false;

    // --- MAGIC BYTES DICTIONARY ---
    if header_bytes.starts_with(b"PK\x03\x04") {
        detected_type = "xlsx/zip".into();
        container_type = "zip".into();
        recommended_action = if ext == "xlsx" || ext == "zip" { "proceed".into() } else { "warn_extension".into() };
    } else if header_bytes.starts_with(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1") {
        detected_type = "xls_legacy".into();
        container_type = "ole2".into();
    } else if header_bytes.starts_with(b"SQLite format 3\x00") {
        detected_type = "sqlite".into();
        container_type = "db".into();
        risk_level = "medium".into();
        recommended_action = "extract_db".into();
    } else if contains_subslice(header_bytes, b"<?xml") && (contains_subslice(header_bytes, b"progid=\"Excel.Sheet\"") || contains_subslice(header_bytes, b"urn:schemas-microsoft-com:office:spreadsheet")) {
        detected_type = "xml_spreadsheet_2003".into();
        container_type = "xml".into();
        risk_level = "high".into();
        can_auto_convert = true;
        recommended_action = "auto_convert".into();
        notes.push("Falso XLS detectado (Estrutura XML nativa do SAP Business One).".into());
    } else if contains_subslice(header_bytes, b"<table") && contains_subslice(header_bytes, b"<tr") {
        detected_type = "html_table".into();
        container_type = "html".into();
        can_auto_convert = true;
        recommended_action = "auto_convert".into();
        notes.push("Falso XLS detectado (Tabela HTML).".into());
    } else if header_bytes.starts_with(b"{") || (header_bytes.starts_with(b"[") && contains_subslice(header_bytes, b"\"")) {
        detected_type = "json".into();
        container_type = "text/json".into();
    } else if header_bytes.starts_with(b"MZ") {
        detected_type = "pe_executable_dll".into();
        container_type = "binary".into();
        risk_level = "critical".into();
        notes.push("Alerta de Segurança: Arquivo executável/binário do Windows detectado!".into());
    } else if header_bytes.starts_with(b"\x7fELF") {
        detected_type = "elf_executable".into();
        container_type = "binary".into();
        risk_level = "critical".into();
        notes.push("Alerta de Segurança: Arquivo executável/binário Linux detectado!".into());
    } else if header_bytes.starts_with(b"PAR1") {
        detected_type = "parquet".into();
        container_type = "binary/columnar".into();
        notes.push("Formato Columnar Big Data (Parquet) identificado.".into());
    } else if header_bytes.starts_with(b"%PDF-") {
        detected_type = "pdf".into();
        container_type = "document".into();
        notes.push("Documento PDF identificado. A extração de dados pode requerer OCR ou parsers complexos.".into());
    } else if trim_start(header_bytes).starts_with(b"<?xml") {
        detected_type = "xml_generic".into();
        container_type = "xml".into();
    } else {
        detected_type = "csv_or_text".into();
        if contains_subslice(header_bytes, b"\t") && contains_subslice(header_bytes, b"\n") {
             detected_type = "tsv_tabulated".into();
             notes.push("Delimitador provável: TAB (Planilha Textual)".into());
        } else if contains_subslice(header_bytes, b";") {
            notes.push("Delimitador provável: Ponto e Vírgula (;)".into());
        } else if contains_subslice(header_bytes, b",") {
            notes.push("Delimitador provável: Vírgula (,)".into());
        }
    }

    if detected_type != "csv_or_text" && (ext == "csv" || ext == "txt") {
        risk_level = "high".into();
        notes.push("Conflito severo de extensão: Arquivo binário mascarado como texto.".into());
    } else if (detected_type == "xml_spreadsheet_2003" || detected_type == "html_table") && ext == "xls" {
        risk_level = "medium".into();
    }

    let report = InspectionReport {
        declared_type: ext,
        detected_type,
        risk_level,
        recommended_action,
        can_auto_convert,
        preview_summary: "".into(),
        encoding_status: "utf-8".into(),
        container_type,
        notes,
    };

    let json = serde_json::to_string(&report)?;
    println!("{}", json);

    Ok(())
}

fn contains_subslice(haystack: &[u8], needle: &[u8]) -> bool {
    haystack.windows(needle.len()).any(|window| window == needle)
}

fn trim_start(haystack: &[u8]) -> &[u8] {
    let mut start = 0;
    while start < haystack.len() && haystack[start].is_ascii_whitespace() {
        start += 1;
    }
    &haystack[start..]
}
