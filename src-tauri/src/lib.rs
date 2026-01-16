use std::fs;
use std::path::Path;
use std::process::Command;
#[cfg(windows)]
use std::os::windows::process::CommandExt;
use tauri_plugin_shell::ShellExt;
use tauri::{Manager, WebviewBuilder, WebviewUrl, LogicalPosition, LogicalSize};
use serde::{Serialize, Deserialize};
use reqwest::Client;

// Windows flag to hide console window
#[cfg(windows)]
const CREATE_NO_WINDOW: u32 = 0x08000000;

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
async fn open_program(program: String, path: String) -> Result<String, String> {
    // Map common program names to their executable paths
    let exe_path = match path.as_str() {
        "winword" => {
            // Try common Office paths
            let paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
            ];
            paths.iter().find(|p| Path::new(p).exists()).map(|s| s.to_string())
        },
        "excel" => {
            let paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
            ];
            paths.iter().find(|p| Path::new(p).exists()).map(|s| s.to_string())
        },
        "powerpnt" => {
            let paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
            ];
            paths.iter().find(|p| Path::new(p).exists()).map(|s| s.to_string())
        },
        "outlook" => {
            let paths = [
                r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
                r"C:\Program Files (x86)\Microsoft Office\root\Office16\OUTLOOK.EXE",
            ];
            paths.iter().find(|p| Path::new(p).exists()).map(|s| s.to_string())
        },
        "ms-teams" => {
            // Teams is typically in LocalAppData
            if let Ok(local_app_data) = std::env::var("LOCALAPPDATA") {
                let teams_path = format!(r"{}\Microsoft\Teams\current\Teams.exe", local_app_data);
                if Path::new(&teams_path).exists() {
                    Some(teams_path)
                } else {
                    None
                }
            } else {
                None
            }
        },
        _ => None, // Fall back to using the path directly
    };

    // Use the resolved path or fall back to original
    let final_path = exe_path.unwrap_or_else(|| path.clone());

    // Launch the program
    let result = Command::new("cmd")
        .args(["/C", "start", "", &final_path])
        .spawn();

    match result {
        Ok(_) => Ok(format!("Launched {}", program)),
        Err(e) => Err(format!("Failed to launch {}: {}", program, e))
    }
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
    let mut cmd = Command::new("powershell");
    cmd.args(["-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", &script_path]);

    // On Windows, hide the console window
    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    let output = cmd.output().map_err(|e| e.to_string())?;

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

    // Use python.exe (not pythonw) to capture output
    let mut cmd = Command::new("python");
    cmd.arg(&script_path);

    // Add target path as argument if provided
    if let Some(target) = &target_path {
        cmd.arg(target);
    }

    // Set working directory
    cmd.current_dir(Path::new(&script_path).parent().unwrap_or(Path::new(".")));

    // On Windows, hide the console window but still capture output
    #[cfg(windows)]
    cmd.creation_flags(CREATE_NO_WINDOW);

    // Execute and capture output (blocking)
    let output = cmd.output()
        .map_err(|e| format!("Failed to execute: {}", e))?;

    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();

    if !output.status.success() {
        if !stderr.is_empty() {
            return Err(format!("Script error:\n{}", stderr));
        }
        return Err(format!("Script failed with exit code: {:?}", output.status.code()));
    }

    // Return stdout, or stderr if stdout is empty
    if !stdout.is_empty() {
        Ok(stdout)
    } else if !stderr.is_empty() {
        Ok(format!("[stderr]\n{}", stderr))
    } else {
        Ok("Script completed (no output)".to_string())
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
    println!("=== chat_with_claude called ===");
    println!("Message: {}", &message[..message.len().min(100)]);
    println!("Context provided: {}", context.is_some());

    // Read API key from file
    let api_key_path = "G:\\My Drive\\00 - Trajanus USA\\00-Command-Center\\001 Credentials\\Trajanus Command Center api key.txt";
    println!("Reading API key from: {}", api_key_path);

    let api_key = fs::read_to_string(api_key_path)
        .map_err(|e| {
            println!("ERROR reading API key: {}", e);
            format!("Failed to read API key: {}", e)
        })?
        .trim()
        .to_string();

    println!("API key loaded, length: {}", api_key.len());

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

    println!("Total messages: {}", messages.len());

    let request_body = ClaudeRequest {
        model: "claude-sonnet-4-20250514".to_string(),
        max_tokens: 1024,
        messages,
    };

    println!("Making API request...");
    let client = Client::new();
    let response = client
        .post("https://api.anthropic.com/v1/messages")
        .header("Content-Type", "application/json")
        .header("x-api-key", &api_key)
        .header("anthropic-version", "2023-06-01")
        .json(&request_body)
        .send()
        .await
        .map_err(|e| {
            println!("ERROR: API request failed: {}", e);
            format!("API request failed: {}", e)
        })?;

    let status = response.status();
    println!("Response status: {}", status);

    if !status.is_success() {
        let error_text = response.text().await.unwrap_or_default();
        println!("ERROR: API error: {}", &error_text[..error_text.len().min(500)]);
        return Err(format!("API error ({}): {}", status, error_text));
    }

    let body = response.text().await.map_err(|e| format!("Failed to read response: {}", e))?;
    println!("Response body length: {}", body.len());

    let claude_response: ClaudeResponse = serde_json::from_str(&body)
        .map_err(|e| {
            println!("ERROR parsing JSON: {}", e);
            format!("Failed to parse response: {}", e)
        })?;

    // Extract text from response
    let text = claude_response
        .content
        .iter()
        .filter_map(|block| block.text.clone())
        .collect::<Vec<_>>()
        .join("\n");

    println!("Success! Response length: {}", text.len());
    Ok(text)
}

// ==================== EMBEDDED WEBVIEW ====================

#[tauri::command]
async fn embed_claude(app: tauri::AppHandle, x: f64, y: f64, width: f64, height: f64) -> Result<(), String> {
    embed_url(app, "https://claude.ai".to_string(), x, y, width, height).await
}

#[tauri::command]
async fn embed_url(app: tauri::AppHandle, url: String, x: f64, y: f64, width: f64, height: f64) -> Result<(), String> {
    // Close existing embedded webview if present
    if let Some(existing) = app.get_webview("embedded-webview") {
        existing.close().map_err(|e| e.to_string())?;
    }
    // Also close old claude-embedded for backwards compatibility
    if let Some(existing) = app.get_webview("claude-embedded") {
        existing.close().map_err(|e| e.to_string())?;
    }

    // Get the WebviewWindow first, then extract the Window
    let webview_window = app.get_webview_window("main")
        .ok_or("Main window not found")?;

    // Get the underlying Window to add child webview
    let main_window = webview_window.as_ref().window();

    // Parse the URL
    let parsed_url: tauri::Url = url.parse().map_err(|e: <tauri::Url as std::str::FromStr>::Err| e.to_string())?;

    // Add as child webview INSIDE main window
    main_window.add_child(
        WebviewBuilder::new(
            "embedded-webview",
            WebviewUrl::External(parsed_url)
        )
        .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        .auto_resize(),
        LogicalPosition::new(x, y),
        LogicalSize::new(width, height),
    ).map_err(|e| e.to_string())?;

    Ok(())
}

#[tauri::command]
async fn close_embedded(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(webview) = app.get_webview("embedded-webview") {
        webview.close().map_err(|e| e.to_string())?;
    }
    // Also close old claude-embedded for backwards compatibility
    if let Some(webview) = app.get_webview("claude-embedded") {
        webview.close().map_err(|e| e.to_string())?;
    }
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
async fn resize_embedded(app: tauri::AppHandle, x: f64, y: f64, width: f64, height: f64) -> Result<(), String> {
    if let Some(webview) = app.get_webview("embedded-webview") {
        webview.set_position(LogicalPosition::new(x, y)).map_err(|e| e.to_string())?;
        webview.set_size(LogicalSize::new(width, height)).map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
async fn is_claude_embedded(app: tauri::AppHandle) -> bool {
    app.get_webview("claude-embedded").is_some()
}

// ==================== QUAD CHAT - MULTIPLE CLAUDE WEBVIEWS ====================

/// Enable quad chat mode - creates 3 Claude.ai webviews alongside the main app
/// Layout: Main app shrinks to top-left, 3 Claude panels fill the rest
#[tauri::command]
async fn enable_quad_chat(app: tauri::AppHandle) -> Result<String, String> {
    println!("=== Enabling Quad Chat Mode ===");

    // Get the main window
    let webview_window = app.get_webview_window("main")
        .ok_or("Main window not found")?;

    let main_window = webview_window.as_ref().window();

    // Get window size
    let size = main_window.inner_size().map_err(|e| e.to_string())?;
    let width = size.width as f64;
    let height = size.height as f64;

    println!("Window size: {}x{}", width, height);

    // Calculate panel sizes (2x2 grid)
    let panel_width = width / 2.0;
    let panel_height = height / 2.0;

    // User agent for Claude.ai
    let user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";

    // Close existing quad chat webviews if they exist
    for label in ["claude-quad-1", "claude-quad-2", "claude-quad-3"] {
        if let Some(existing) = app.get_webview(label) {
            let _ = existing.close();
        }
    }

    // WEBVIEW 1: Claude.ai Chat 1 (top-right)
    main_window.add_child(
        WebviewBuilder::new(
            "claude-quad-1",
            WebviewUrl::External("https://claude.ai".parse().unwrap()),
        )
        .user_agent(user_agent)
        .auto_resize(),
        LogicalPosition::new(panel_width, 0.0),
        LogicalSize::new(panel_width, panel_height),
    ).map_err(|e| format!("Failed to create claude-quad-1: {}", e))?;

    println!("Created claude-quad-1 at ({}, 0) size {}x{}", panel_width, panel_width, panel_height);

    // WEBVIEW 2: Claude.ai Chat 2 (bottom-left)
    main_window.add_child(
        WebviewBuilder::new(
            "claude-quad-2",
            WebviewUrl::External("https://claude.ai".parse().unwrap()),
        )
        .user_agent(user_agent)
        .auto_resize(),
        LogicalPosition::new(0.0, panel_height),
        LogicalSize::new(panel_width, panel_height),
    ).map_err(|e| format!("Failed to create claude-quad-2: {}", e))?;

    println!("Created claude-quad-2 at (0, {}) size {}x{}", panel_height, panel_width, panel_height);

    // WEBVIEW 3: Claude.ai Chat 3 (bottom-right)
    main_window.add_child(
        WebviewBuilder::new(
            "claude-quad-3",
            WebviewUrl::External("https://claude.ai".parse().unwrap()),
        )
        .user_agent(user_agent)
        .auto_resize(),
        LogicalPosition::new(panel_width, panel_height),
        LogicalSize::new(panel_width, panel_height),
    ).map_err(|e| format!("Failed to create claude-quad-3: {}", e))?;

    println!("Created claude-quad-3 at ({}, {}) size {}x{}", panel_width, panel_height, panel_width, panel_height);

    // Resize the main webview to top-left quadrant
    if let Some(main_webview) = app.get_webview("main") {
        main_webview.set_position(LogicalPosition::new(0.0, 0.0)).map_err(|e| e.to_string())?;
        main_webview.set_size(LogicalSize::new(panel_width, panel_height)).map_err(|e| e.to_string())?;
        println!("Resized main webview to top-left quadrant");
    }

    Ok("Quad Chat Mode enabled - 3 Claude.ai panels created".to_string())
}

/// Disable quad chat mode - closes all Claude webviews and restores main app to full size
#[tauri::command]
async fn disable_quad_chat(app: tauri::AppHandle) -> Result<String, String> {
    println!("=== Disabling Quad Chat Mode ===");

    // Close all quad chat webviews
    for label in ["claude-quad-1", "claude-quad-2", "claude-quad-3"] {
        if let Some(webview) = app.get_webview(label) {
            webview.close().map_err(|e| format!("Failed to close {}: {}", label, e))?;
            println!("Closed {}", label);
        }
    }

    // Get the main window to restore size
    let webview_window = app.get_webview_window("main")
        .ok_or("Main window not found")?;

    let main_window = webview_window.as_ref().window();
    let size = main_window.inner_size().map_err(|e| e.to_string())?;

    // Restore main webview to full size
    if let Some(main_webview) = app.get_webview("main") {
        main_webview.set_position(LogicalPosition::new(0.0, 0.0)).map_err(|e| e.to_string())?;
        main_webview.set_size(LogicalSize::new(size.width as f64, size.height as f64)).map_err(|e| e.to_string())?;
        println!("Restored main webview to full size");
    }

    Ok("Quad Chat Mode disabled".to_string())
}

/// Check if quad chat mode is active
#[tauri::command]
async fn is_quad_chat_enabled(app: tauri::AppHandle) -> bool {
    app.get_webview("claude-quad-1").is_some()
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
            open_program,
            open_terminal,
            launch_vscode,
            launch_git_bash,
            launch_claude_code,
            git_push,
            run_powershell_script,
            run_python_script,
            chat_with_claude,
            embed_claude,
            embed_url,
            close_claude,
            close_embedded,
            resize_claude,
            resize_embedded,
            is_claude_embedded,
            enable_quad_chat,
            disable_quad_chat,
            is_quad_chat_enabled
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
