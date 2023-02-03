# robotit

## Python

```bash
pip install easyocr
pip install pyautogui
```

## CPython

https://github.com/dgrunwald/rust-cpython

```rust
use cpython::{Python, PyDict, PyResult};

fn hello(py: Python) -> PyResult<()> {
    let sys = py.import("sys")?;
    let version: String = sys.get(py, "version")?.extract(py)?;

    let locals = PyDict::new(py);
    locals.set_item(py, "os", py.import("os")?)?;
    let user: String = py.eval("os.getenv('USER') or os.getenv('USERNAME')", None, Some(&locals))?.extract(py)?;
    py.run("/Users/qianzhaoyi/Projects/Kit/Games/robotit/tt.py", None, Some(&locals)).unwrap();

    println!("Hello {}, I'm Python {}", user, version);
    Ok(())
}
```

```bash
PYTHON_SYS_EXECUTABLE=/opt/homebrew/opt/python@3.10/libexec/bin/python cargo tauri dev
```

## PyO3

https://github.com/PyO3/pyo3

```rust
use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

fn test_py() -> PyResult<()> {
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let version: String = sys.getattr("version")?.extract()?;

        let locals = [("os", py.import("os")?)].into_py_dict(py);
        let code = "os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'";
        let user: String = py.eval(code, None, Some(&locals))?.extract()?;

        println!("Hello {}, I'm Python {}", user, version);
        Ok(())
    })
}
```

```bash
PYO3_PYTHON=/opt/homebrew/opt/python@3.10/libexec/bin/python cargo tauri dev

PYO3_PYTHON=/Users/qianzhaoyi/Projects/Kit/Games/robotit/.venv/bin/python cargo tauri dev
```