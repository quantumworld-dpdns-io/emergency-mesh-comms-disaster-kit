import { render, screen } from "@testing-library/react";
import StatusDashboard from "../components/StatusDashboard";

test("shows status card", () => {
  render(<StatusDashboard />);
  expect(screen.getByText("Status")).toBeInTheDocument();
});
