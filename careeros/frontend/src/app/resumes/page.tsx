"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { resumeService } from "@/services";
import { aiService } from "@/services/ai";
import { FileText, Plus, Trash2, Star, Upload, Sparkles } from "lucide-react";
import type { ResumeResponse } from "@/types";

export default function ResumesPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [isCreating, setIsCreating] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: resumes = [], isLoading } = useQuery({
    queryKey: ["resumes"],
    queryFn: () => resumeService.getResumes(),
    enabled: !!user,
  });

  const createMutation = useMutation({
    mutationFn: (data: { title: string; content: string }) =>
      resumeService.createResume({
        title: data.title,
        content: data.content,
        is_primary: false,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
      setIsCreating(false);
      setNewTitle("");
      setNewContent("");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => resumeService.deleteResume(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
    },
  });

  const setPrimaryMutation = useMutation({
    mutationFn: (id: string) => resumeService.setPrimaryResume(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resumes"] });
    },
  });

  const handleAnalyzeATS = async (resume: ResumeResponse) => {
    try {
      const result = await aiService.analyzeResume({
        resume_content: resume.content,
        resume_id: resume.id,
      });
      alert(`ATS Score: ${result.ats_score}/100\n\nImprovements:\n${result.improvements.join("\n")}`);
    } catch (error: unknown) {
      if (error instanceof Error) {
        alert(`Failed to analyze resume: ${error.message}`);
      }
    }
  };

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;
    createMutation.mutate({ title: newTitle, content: newContent });
  };

  if (authLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            My Resumes
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Create, manage, and optimize your resumes with AI.
          </p>
        </div>
        <button
          onClick={() => setIsCreating(true)}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          New Resume
        </button>
      </div>

      {/* Create Resume Form */}
      {isCreating && (
        <div className="mb-8 p-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold mb-4">Create New Resume</h2>
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Title</label>
              <input
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="e.g., Software Engineer Resume"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary dark:bg-gray-700"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Content</label>
              <textarea
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                placeholder="Paste your resume content here..."
                rows={10}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary dark:bg-gray-700"
              />
            </div>
            <div className="flex gap-2">
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50"
              >
                {createMutation.isPending ? "Creating..." : "Create"}
              </button>
              <button
                type="button"
                onClick={() => setIsCreating(false)}
                className="px-4 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Resumes Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 animate-pulse"
            >
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          ))}
        </div>
      ) : resumes.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No resumes yet
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Create your first resume to get started.
          </p>
          <button
            onClick={() => setIsCreating(true)}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            Create Resume
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                    {resume.title}
                  </h3>
                  {resume.is_primary && (
                    <span className="inline-flex items-center px-2 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 text-xs rounded">
                      <Star className="w-3 h-3 mr-1" />
                      Primary
                    </span>
                  )}
                </div>
              </div>

              {resume.ats_score !== null && resume.ats_score !== undefined && (
                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-gray-600 dark:text-gray-400">ATS Score</span>
                    <span className="font-semibold">{resume.ats_score}/100</span>
                  </div>
                  <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        resume.ats_score >= 80
                          ? "bg-green-500"
                          : resume.ats_score >= 60
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${resume.ats_score}%` }}
                    />
                  </div>
                </div>
              )}

              <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 mb-4">
                {resume.content.slice(0, 150)}...
              </p>

              <div className="flex gap-2">
                {!resume.is_primary && (
                  <button
                    onClick={() => setPrimaryMutation.mutate(resume.id)}
                    className="flex-1 px-3 py-2 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 rounded-lg hover:bg-yellow-200 dark:hover:bg-yellow-900/50 transition-colors text-sm font-medium flex items-center justify-center gap-1"
                  >
                    <Star className="w-4 h-4" />
                    Set Primary
                  </button>
                )}
                <button
                  onClick={() => handleAnalyzeATS(resume)}
                  className="flex-1 px-3 py-2 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 rounded-lg hover:bg-purple-200 dark:hover:bg-purple-900/50 transition-colors text-sm font-medium flex items-center justify-center gap-1"
                >
                  <Sparkles className="w-4 h-4" />
                  Analyze
                </button>
                <button
                  onClick={() => deleteMutation.mutate(resume.id)}
                  disabled={deleteMutation.isPending}
                  className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors disabled:opacity-50"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
