-- Life Tracker Database Schema
-- Run this in your Supabase SQL editor to set up the tables

-- Inbox table: stores raw captures before processing
CREATE TABLE inbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_text TEXT NOT NULL,
    classification JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Goals table: stores larger, multi-week goals
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,
    progress FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table: stores concrete, actionable tasks
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    urgency_bucket TEXT NOT NULL CHECK (urgency_bucket IN ('today', 'this_week', 'this_month', 'bucket')),
    loose_deadline TEXT,
    linked_goal_id UUID REFERENCES goals(id) ON DELETE SET NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_inbox_processed ON inbox(processed);
CREATE INDEX idx_inbox_created_at ON inbox(created_at DESC);
CREATE INDEX idx_tasks_urgency_bucket ON tasks(urgency_bucket);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_linked_goal ON tasks(linked_goal_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_goals_created_at ON goals(created_at DESC);

-- Enable Row Level Security (optional - configure based on your auth needs)
ALTER TABLE inbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- Default policy: allow all for now (adjust based on auth requirements)
CREATE POLICY "Allow all operations" ON inbox FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON goals FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON tasks FOR ALL USING (true);
