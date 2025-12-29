use std::fs;
use std::path::Path;
use std::process::Command;
use tauri_plugin_shell::ShellExt;
use tauri::{Manager, WebviewBuilder, WebviewUrl, LogicalPosition, LogicalSize};
use serde::{Serialize, Deserialize};
use reqwest::Client;

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

// ==================== CLAUDE API ====================

#[derive(Serialize)]
struct ClaudeMessage {
    role: String,
    content: String,
}

#[derive(Serialize)]
struct ClaudeRequest {
    model: String,
    max_tokens: u32,
    messages: Vec<ClaudeMessage>,
}

#[derive(Deserialize)]
struct ClaudeContentBlock {
    #[serde(rename = "type")]
    content_type: String,
    text: Option<String>,
}

#[derive(Deserialize)]
struct ClaudeResponse {
    content: Vec<ClaudeContentBlock>,
}

#[tauri::command]
async fn chat_with_claude(message: String, context: Option<String>) -> Result<String, String> {
    // Read API key from file
    let api_key_path = "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\001 Credentials\\Trajanus Command Center api key.txt";
    let api_key = fs::read_to_string(api_key_path)
        .map_err(|e| format!("Failed to read API key: {}", e))?
        .trim()
        .to_string();

    // Build messages array
    let mut messages = Vec::new();

    // Add context as system-like user message if provided
    if let Some(ctx) = context {
        messages.push(ClaudeMessage {
            role: "user".to_string(),
            content: format!("Context for this conversation:\n{}\n\nNow, please respond to my next message.", ctx),
        });
        messages.push(ClaudeMessage {
            role: "assistant".to_string(),
            content: "I understand. I'll use that context to help with your questions. What would you like to know?".to_string(),
        });
    }

    // Add the user's message
    messages.push(ClaudeMessage {
        role: "user".to_string(),
        content: message,
    });

    let request_body = ClaudeRequest {
        model: "claude-sonnet-4-5-20250929".to_string(),
        max_tokens: 1024,
        messages,
    };

    let client = Client::new();
    let response = client
        .post("https://api.anthropic.com/v1/messages")
        .header("Content-Type", "application/json")
        .header("x-api-key", &api_key)
        .header("anthropic-version", "2023-06-01")
        .json(&request_body)
        .send()
        .await
        .map_err(|e| format!("API request failed: {}", e))?;

    if !response.status().is_success() {
        let error_text = response.text().await.unwrap_or_default();
        return Err(format!("API error: {}", error_text));
    }

    let claude_response: ClaudeResponse = response
        .json()
        .await
        .map_err(|e| format!("Failed to parse response: {}", e))?;

    // Extract text from response
    let text = claude_response
        .content
        .iter()
        .filter_map(|block| block.text.clone())
        .collect::<Vec<_>>()
        .join("\n");

    Ok(text)
}

// ==================== EMBEDDED CLAUDE WEBVIEW ====================

#[tauri::command]
async fn embed_claude(app: tauri::AppHandle, x: f64, y: f64, width: f64, height: f64) -> Result<(), String> {
    // Close existing claude webview if present
    if let Some(existing) = app.get_webview("claude-embedded") {
        existing.close().map_err(|e| e.to_string())?;
    }

    // Get the WebviewWindow first, then extract the Window
    let webview_window = app.get_webview_window("main")
        .ok_or("Main window not found")?;

    // Get the underlying Window to add child webview
    let main_window = webview_window.as_ref().window();

    // Add Claude as child webview INSIDE main window
    main_window.add_child(
        WebviewBuilder::new(
            "claude-embedded",
            WebviewUrl::External("https://claude.ai".parse().unwrap())
        )
        .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        .auto_resize(),
        LogicalPosition::new(x, y),
        LogicalSize::new(width, height),
    ).map_err(|e| e.to_string())?;

    Ok(())
}

#[tauri::command]
async fn close_claude(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(webview) = app.get_webview("claude-embedded") {
        webview.close().map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
async fn resize_claude(app: tauri::AppHandle, x: f64, y: f64, width: f64, height: f64) -> Result<(), String> {
    if let Some(webview) = app.get_webview("claude-embedded") {
        webview.set_position(LogicalPosition::new(x, y)).map_err(|e| e.to_string())?;
        webview.set_size(LogicalSize::new(width, height)).map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
async fn is_claude_embedded(app: tauri::AppHandle) -> bool {
    app.get_webview("claude-embedded").is_some()
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
            run_python_script,
            chat_with_claude,
            embed_claude,
            close_claude,
            resize_claude,
            is_claude_embedded
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
