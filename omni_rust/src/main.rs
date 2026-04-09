mod inspect;
mod convert;

use clap::{Parser, Subcommand};
use std::process;

#[derive(Parser)]
#[command(name = "genaja_omni")]
#[command(about = "Motor Genaja de Inspeção e Conversão Omni-Data nativo", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Inspeciona o arquivo por magic bytes
    Inspect {
        /// Caminho absoluto ou relativo para o arquivo
        path: String,
    },
    /// Converte um arquivo baseado no tipo detectado
    Convert {
        /// Caminho para o arquivo de origem
        in_path: String,
        /// Tipo detectado na inspecao
        detected_type: String,
        /// Caminho para salvar a extração final
        out_path: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Inspect { path } => {
            if let Err(e) = inspect::run_inspection(path) {
                eprintln!("{{\"error\": \"Error running inspect: {}\"}}", e);
                process::exit(1);
            }
        }
        Commands::Convert { in_path, detected_type, out_path } => {
            if let Err(e) = convert::run_conversion(in_path, detected_type, out_path) {
                eprintln!("{{\"success\": false, \"warnings\": [\"Error running convert: {}\"]}}", e);
                process::exit(1);
            }
        }
    }
}
