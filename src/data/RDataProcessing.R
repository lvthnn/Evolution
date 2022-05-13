# Import required packages
library(tidyverse)

# Read CSV file into DataFrame
f <- file.path('~/Github/Evolution/src/data/data-medphi-loDphi-medlambda.csv')
data <- data.table::fread(f)


# Create linear fit object of average fitness
# over environmental difficulty
rho <- cor(data$avg_fitness, data$difficulty)

# Data visualization
plot <- ggplot(data, aes(x = difficulty, y = avg_fitness)) +
  geom_point(
    shape = 21, 
    alpha = 0.1,
    position = position_jitter(width = 0.2),
    color = "black"
  ) +
  geom_smooth(color = "black") +
  theme_classic() +
  labs(
    x = "Umhverfisþáttur",
    y = "Meðalhæfni"
  ) +
  theme(
    text = element_text(size = 18)
  ) +
  annotate("text", x = 2, y = 1.15, label = "ρ = 0.844455", size = 6)

ggsave("~/Github/Evolution/src/notes/img/plotA.png", plot, width = 6, height = 6)
