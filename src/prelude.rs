pub use crate::{error::Error, log::Log};

pub type Result<T> = std::result::Result<T, Error>;
