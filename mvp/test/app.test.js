const request = require("supertest");
const path = require("path");
const fs = require("fs");
const app = require("../server/app");

describe("MVP server", () => {
  it("responds to ping", async () => {
    const res = await request(app).get("/api/ping");
    expect(res.statusCode).toBe(200);
    expect(res.body.ok).toBeTruthy();
  });

  it("can login and fetch a protected report", async () => {
    // Register and login as therapist
    const reg = await request(app)
      .post("/api/register")
      .send({ username: "therapist", password: "testpass", role: "therapist" });
    // If the user already exists (tests re-run), accept 200 or 409 (conflict)
    expect([200, 409]).toContain(reg.statusCode);
    const loginRes = await request(app)
      .post("/api/login")
      .send({ username: "therapist", password: "testpass" });
    expect(loginRes.statusCode).toBe(200);
    expect(loginRes.body.token).toBeTruthy();
    const token = loginRes.body.token;

    // post a message
    const chatRes = await request(app)
      .post("/api/chat")
      .send({ client_id: "test-client-1", message: "I had a craving now" });
    expect(chatRes.statusCode).toBe(200);
    expect(chatRes.body.reply).toBeTruthy();

    // get the protected report
    const reportRes = await request(app)
      .get("/api/report/test-client-1")
      .set("Authorization", `Bearer ${token}`);
    expect(reportRes.statusCode).toBe(200);
    expect(reportRes.body.client_id).toBe("test-client-1");
  });

  it("denies non-therapist access to report", async () => {
    // register a client user and get token
    await request(app)
      .post("/api/register")
      .send({ username: "regular", password: "p", role: "client" });
    const loginRes = await request(app)
      .post("/api/login")
      .send({ username: "regular", password: "p" });
    const token = loginRes.body.token;
    const res = await request(app)
      .get("/api/report/test-client-1")
      .set("Authorization", `Bearer ${token}`);
    expect(res.statusCode).toBe(403);
  });

  it("private messages are only visible to therapist", async () => {
    // post a private message
    await request(app)
      .post("/api/chat")
      .send({ client_id: "p-client", message: "private note", private: true });

    // therapist can fetch report
    await request(app)
      .post("/api/register")
      .send({ username: "thera", password: "secret", role: "therapist" });
    const t = await request(app)
      .post("/api/login")
      .send({ username: "thera", password: "secret" });
    const trep = await request(app)
      .get("/api/report/p-client")
      .set("Authorization", `Bearer ${t.body.token}`);
    expect(trep.statusCode).toBe(200);
    expect(
      trep.body.messages.some((m) => m.message === "private note")
    ).toBeTruthy();

    // client role should be forbidden
    await request(app)
      .post("/api/register")
      .send({ username: "cli", password: "pass", role: "client" });
    const c = await request(app)
      .post("/api/login")
      .send({ username: "cli", password: "pass" });
    const crep = await request(app)
      .get("/api/report/p-client")
      .set("Authorization", `Bearer ${c.body.token}`);
    expect(crep.statusCode).toBe(403);
  });

  it("can log cravings and fetch resources", async () => {
    const cravingRes = await request(app)
      .post("/api/craving")
      .send({ client_id: "test-client-2", severity: 2, note: "testing" });
    expect(cravingRes.statusCode).toBe(200);
    expect(cravingRes.body.ok).toBeTruthy();

    const resRes = await request(app).get("/api/resources");
    expect(resRes.statusCode).toBe(200);
    expect(Array.isArray(resRes.body.resources)).toBeTruthy();
  });
});
