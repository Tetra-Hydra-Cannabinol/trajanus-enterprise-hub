use std::fs;
use std::path::Path;
use std::process::Command;
use tauri_plugin_shell::ShellExt;
use serde::Serialize;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct DirEntry {
    name: String,
    path: String,
    is_dir: bool,
}

#[tauri::command]
fn list_directory(path: String) -> Result<Vec<DirEntry>, String> {
    let dir_path = Path::new(&path);
    if !dir_path.exists() {
        return Err(format!("Path not found: {}", path));
    }
    if !dir_path.is_dir() {
        return Err(format!("Not a directory: {}", path));
    }

    let mut entries: Vec<DirEntry> = Vec::new();

    for entry in fs::read_dir(dir_path).map_err(|e| e.to_string())? {
        let entry = entry.map_err(|e| e.to_string())?;
        let metadata = entry.metadata().map_err(|e| e.to_string())?;

        entries.push(DirEntry {
            name: entry.file_name().to_string_lossy().to_string(),
            path: entry.path().to_string_lossy().to_string(),
            is_dir: metadata.is_dir(),
        });
    }

    // Sort: directories first, then by name
    entries.sort_by(|a, b| {
        match (a.is_dir, b.is_dir) {
            (true, false) => std::cmp::Ordering::Less,
            (false, true) => std::cmp::Ordering::Greater,
            _ => a.name.to_lowercase().cmp(&b.name.to_lowercase()),
        }
    });

    Ok(entries)
}

#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
async fn open_path(app: tauri::AppHandle, path: String) -> Result<(), String> {
    app.shell().open(&path, None).map_err(|e| e.to_string())
}

#[tauri::command]
fn open_terminal(path: String) -> Result<(), String> {
    Command::new("powershell")
        .args(["-NoExit", "-Command", &format!("cd \"{}\"", path)])
        .spawn()
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn launch_vscode(path: String) -> Result<(), String> {
    Command::new("code")
        .arg(&path)
        .spawn()
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn launch_git_bash(path: String) -> Result<(), String> {
    Command::new("C:\\Program Files\\Git\\git-bash.exe")
        .arg(format!("--cd={}", path))
        .spawn()
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn launch_claude_code(path: String) -> Result<(), String> {
    // Try to launch claude in a new terminal window
    Command::new("cmd")
        .args(["/c", "start", "cmd", "/k", &format!("cd /d \"{}\" && claude", path)])
        .spawn()
        .map_err(|e| e.to_string())?;
    Ok(())
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    if let Some(parent) = Path::new(&path).parent() {
        fs::create_dir_all(parent).map_err(|e| e.to_string())?;
    }
    fs::write(&path, content).map_err(|e| e.to_string())
}

#[tauri::command]
fn file_exists(path: String) -> bool {
    Path::new(&path).exists()
}

#[tauri::command]
fn git_push(path: String) -> Result<String, String> {
    let output = Command::new("git")
        .current_dir(&path)
        .args(["add", "-A"])
        .output()
        .map_err(|e| e.to_string())?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }

    let output = Command::new("git")
        .current_dir(&path)
        .args(["commit", "-m", "Auto-commit from Developer Toolkit"])
        .output()
        .map_err(|e| e.to_string())?;

    let commit_msg = String::from_utf8_lossy(&output.stdout).to_string();

    let output = Command::new("git")
        .current_dir(&path)
        .args(["push"])
        .output()
        .map_err(|e| e.to_string())?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }

    Ok(format!("{}\n{}", commit_msg, String::from_utf8_lossy(&output.stdout)))
}

#[tauri::command]
fn run_powershell_script(script_path: String) -> Result<String, String> {
    let output = Command::new("powershell")
        .args(["-ExecutionPolicy", "Bypass", "-File", &script_path])
        .output()
        .map_err(|e| e.to_string())?;

    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).to_string());
    }

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

#[tauri::command]
fn run_python_script(script_path: String, target_path: Option<String>) -> Result<String, String> {
    // Validate script path exists
    if !Path::new(&script_path).exists() {
        return Err(format!("Script not found: {}", script_path));
    }

    // Build command
    let mut cmd = Command::new("cmd");
    cmd.arg("/k").arg("python").arg(&script_path);

    // Add target path as argument if provided
    if let Some(target) = &target_path {
        cmd.arg(target);
    }

    // Set working directory and spawn
    cmd.current_dir(Path::new(&script_path).parent().unwrap_or(Path::new(".")))
        .spawn()
        .map_err(|e| format!("Failed to execute: {}", e))?;

    match target_path {
        Some(target) => Ok(format!("Launched: {} with target: {}", script_path, target)),
        None => Ok(format!("Launched: {}", script_path)),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            list_directory,
            read_file,
            write_file,
            file_exists,
            open_path,
            open_terminal,
            launch_vscode,
            launch_git_bash,
            launch_claude_code,
            git_push,
            run_powershell_script,
            run_python_script
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
