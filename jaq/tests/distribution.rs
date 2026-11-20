use std::{fs, process::Command};

#[test]
fn module_search_expands_home() {
    let home = tempfile::tempdir().unwrap();
    let modules = home.path().join("modules");
    fs::create_dir(&modules).unwrap();
    fs::write(modules.join("example.jq"), "def answer: 42;").unwrap();
    let output = Command::new(env!("CARGO_BIN_EXE_jaq"))
        .env("HOME", home.path())
        .env_remove("USERPROFILE")
        .args(["-n", "-L", "~/modules", "include \"example\"; answer"])
        .output()
        .unwrap();
    assert!(output.status.success(), "{}", String::from_utf8_lossy(&output.stderr));
    assert_eq!(output.stdout, b"42\n");
}

#[test]
fn repl_filter_is_unavailable() {
    let output = Command::new(env!("CARGO_BIN_EXE_jaq"))
        .args(["-n", "repl"])
        .output()
        .unwrap();
    assert_eq!(output.status.code(), Some(3));
    assert!(output.stdout.is_empty());
    assert!(String::from_utf8_lossy(&output.stderr).contains("undefined filter"));
}

#[cfg(feature = "cbor")]
#[test]
fn cbor_feature_encodes_values() {
    let output = Command::new(env!("CARGO_BIN_EXE_jaq"))
        .args(["-n", "--to", "cbor", "1"])
        .output()
        .unwrap();
    assert!(output.status.success(), "{}", String::from_utf8_lossy(&output.stderr));
    assert_eq!(output.stdout, [1]);
}

