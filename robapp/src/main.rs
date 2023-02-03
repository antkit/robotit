#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    test_py().expect("failed calling python");

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

use pyo3::prelude::*;
// use pyo3::types::IntoPyDict;

fn test_py() -> PyResult<()> {
    // Python::with_gil(|py| {
    //     let sys = py.import("sys")?;
    //     let version: String = sys.getattr("version")?.extract()?;

    //     let locals = [("os", py.import("os")?)].into_py_dict(py);
    //     let code = "os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'";
    //     let user: String = py.eval(code, None, Some(&locals))?.extract()?;

    //     println!("Hello {}, I'm Python {}", user, version);

    //     Ok(())
    // })


    let py_utils = include_str!("/Users/qianzhaoyi/Projects/Kit/Games/robotit/pyscripts/utils/__init__.py");
    let py_common = include_str!("/Users/qianzhaoyi/Projects/Kit/Games/robotit/pyscripts/utils/common.py");
    let py_screen = include_str!("/Users/qianzhaoyi/Projects/Kit/Games/robotit/pyscripts/utils/screen.py");
    let py_app = include_str!("/Users/qianzhaoyi/Projects/Kit/Games/robotit/pyscripts/epic7.py");
    let from_python = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
        py.run(r#"
import sys
print(sys.executable, sys.path)
"#, None, None).unwrap();
        PyModule::from_code(py, py_utils, "utils", "utils")?;
        PyModule::from_code(py, py_common, "utils.common", "utils.common")?;
        PyModule::from_code(py, py_screen, "utils.screen", "utils.screen")?;
        let app: Py<PyAny> = PyModule::from_code(py, py_app, "", "")?
            .getattr("screen_info")?
            .into();
        app.call0(py)
    });

    println!("py: {}", from_python?);
    Ok(())
}
