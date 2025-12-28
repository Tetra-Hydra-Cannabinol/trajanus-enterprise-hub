use std::fs;
use std::path::Path;
use std::process::Command;
use tauri_plugin_shell::ShellExt;

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
fn run_python_script(script_path: String) -> Result<String, String> {
    // Spawn Python script in a new terminal window (non-blocking)
    // This allows scripts with GUI dialogs to work properly
    Command::new("cmd")
        .args(["/c", "start", "cmd", "/k", &format!("python \"{}\"", script_path)])
        .spawn()
        .map_err(|e| e.to_string())?;

    Ok(format!("Launched: {}", script_path))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
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
