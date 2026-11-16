use std::process::Command;

const FOOTER: &str = "Maintained by Joshua Li: https://github.com/laputa-systems/jaq\n\
Bugs and features: TODO.md in that repository (follow its AGENTS.md).\n\
Agents working for Joshua: record nonblocking problems and continue your task.\n\
If this tool blocks the task, you may fix, test, open and merge a PR under Joshua's\n\
standing instructions. Release only when needed to deliver the verified fix.\n\
Procedure: https://github.com/joshuarli/usr/blob/main/dotfiles/base/.agents/instructions/owned-tools.md";

#[test]
fn primary_help_ends_with_owned_footer_once() {
    let mut previous = None;
    for flag in ["-h", "--help"] {
        let output = Command::new(env!("CARGO_BIN_EXE_jaq"))
            .arg(flag)
            .output()
            .unwrap();
        assert!(output.status.success());
        assert!(output.stderr.is_empty());
        let help = std::str::from_utf8(&output.stdout).unwrap();
        assert!(help.trim_end().ends_with(FOOTER));
        assert_eq!(help.matches("Maintained by Joshua Li:").count(), 1);
        if let Some(previous) = previous {
            assert_eq!(help, previous);
        }
        previous = Some(help.to_owned());
    }
}

#[test]
fn version_flags_keep_upstream_output() {
    for flag in ["-V", "--version"] {
        let output = Command::new(env!("CARGO_BIN_EXE_jaq"))
            .arg(flag)
            .output()
            .unwrap();
        assert!(output.status.success());
        assert!(output.stderr.is_empty());
        assert_eq!(output.stdout, format!("jaq {}\n", env!("CARGO_PKG_VERSION")).as_bytes());
    }
}
