use serde::Serialize;
use std::io::{self};
use quick_xml::events::Event;
use quick_xml::Reader;
use std::time::Instant;

#[derive(Serialize)]
pub struct ConversionReport {
    pub success: bool,
    pub output_path: String,
    pub output_type: String,
    pub rows_written: usize,
    pub execution_time_ms: u128,
    pub warnings: Vec<String>,
}

pub fn run_conversion(in_path: &str, detected_type: &str, out_path: &str) -> io::Result<()> {
    let start_time = Instant::now();
    let mut warnings = Vec::new();
    let mut rows_written = 0;
    let mut success = false;
    
    if detected_type == "xml_spreadsheet_2003" {
        match convert_xml_spreadsheet(in_path, out_path) {
            Ok(count) => {
                rows_written = count;
                success = true;
            },
            Err(e) => {
                warnings.push(format!("Fail parsing XML: {}", e));
            }
        }
    } else if detected_type == "csv_or_text" || detected_type == "tsv_tabulated" {
        // Passthrough: copia o arquivo direto para o destino como CSV
        match std::fs::copy(in_path, out_path) {
            Ok(bytes) => {
                rows_written = bytes as usize;
                success = true;
                warnings.push("[Rust] CSV/Texto copiado diretamente (passthrough).".to_string());
            },
            Err(e) => {
                warnings.push(format!("Fail copying file: {}", e));
            }
        }
    } else {
        // Para xlsx, xls_legacy e outros: delegar ao Python Fallback
        // Retornamos success:false para acionar o fallback de forma controlada
        warnings.push(format!("[Rust] Tipo '{}' delegado ao motor Python para conversão avançada.", detected_type));
    }

    let elapsed = start_time.elapsed().as_millis();

    let report = ConversionReport {
        success,
        output_path: out_path.to_string(),
        output_type: "csv".to_string(),
        rows_written,
        execution_time_ms: elapsed,
        warnings,
    };

    let json = serde_json::to_string(&report)?;
    println!("{}", json);

    Ok(())
}

fn convert_xml_spreadsheet(in_path: &str, out_path: &str) -> Result<usize, Box<dyn std::error::Error>> {
    let mut reader = Reader::from_file(in_path)?;
    reader.trim_text(true);

    let mut wtr = csv::WriterBuilder::new().delimiter(b';').from_path(out_path)?;
    let mut buf = Vec::new();
    let mut current_row = Vec::new();
    let mut in_row = false;
    let mut in_data = false;
    let mut rows_written = 0;

    loop {
        match reader.read_event_into(&mut buf) {
            Err(e) => return Err(Box::new(e)),
            Ok(Event::Eof) => break,
            Ok(Event::Start(ref e)) => {
                let name = e.name();
                let tag = name.as_ref();
                let stripped = if let Some(idx) = tag.iter().position(|&b| b == b':') {
                    &tag[idx+1..]
                } else {
                    tag
                };

                if stripped == b"Row" {
                    in_row = true;
                    current_row.clear();
                } else if stripped == b"Data" && in_row {
                    in_data = true;
                }
            },
            Ok(Event::End(ref e)) => {
                let name = e.name();
                let tag = name.as_ref();
                let stripped = if let Some(idx) = tag.iter().position(|&b| b == b':') {
                    &tag[idx+1..]
                } else {
                    tag
                };

                if stripped == b"Data" && in_row {
                    in_data = false;
                } else if stripped == b"Row" {
                    if in_row && !current_row.is_empty() {
                        wtr.write_record(&current_row)?;
                        rows_written += 1;
                    }
                    in_row = false;
                    current_row.clear();
                }
            },
            Ok(Event::Text(e)) => {
                if in_data {
                    let txt = e.unescape()?;
                    current_row.push(txt.into_owned());
                }
            },
            _ => (),
        }
        buf.clear();
    }
    
    wtr.flush()?;
    Ok(rows_written)
}
