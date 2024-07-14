#[derive(Debug, PartialEq, PartialOrd)]
enum LogLevel {
    Info,
    Warning,
    Error,
    None,
}

impl From<u8> for LogLevel {
    fn from(value: u8) -> Self {
        match value {
            0 => Self::Info,
            1 => Self::Warning,
            2 => Self::Error,
            _ => Self::None,
        }
    }
}

pub struct Log {
    log_level: LogLevel,
}

impl Log {
    pub fn new(log_level: u8) -> Self {
        Self {
            log_level: LogLevel::from(log_level),
        }
    }

    pub fn info(&self, msg: &str) {
        if self.log_level <= LogLevel::Info {
            println!("INFO | {}", msg);
        }
    }

    pub fn warning(&self, msg: &str) {
        if self.log_level <= LogLevel::Warning {
            println!("WARNING | {}", msg);
        }
    }

    pub fn error(&self, msg: &str) {
        if self.log_level <= LogLevel::Error {
            println!("ERROR | {}", msg);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn log_level() {
        assert_eq!(LogLevel::Info, LogLevel::from(0));
        assert_eq!(LogLevel::Warning, LogLevel::from(1));
        assert_eq!(LogLevel::Error, LogLevel::from(2));
        assert_eq!(LogLevel::None, LogLevel::from(3));
    }

    #[test]
    fn log() {
        assert_eq!(Log::new(2).log_level, LogLevel::Error);
    }
}
