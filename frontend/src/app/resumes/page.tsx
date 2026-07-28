'use client';

import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from '@/components/ui';
import { resumesService } from '@/services/resumes';
import { aiService } from '@/services/ai';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import type { ResumeResponse, ResumeCreate, ResumeAnalysisRequest } from '@/types';

export default function ResumesPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthContext();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newResumeTitle, setNewResumeTitle] = useState('');
  const [newResumeContent, setNewResumeContent] = useState('');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: resumes = [], isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: () => resumesService.getResumes(),
    enabled: isAuthenticated,
  });

  const createResumeMutation = useMutation({
    mutationFn: (data: ResumeCreate) => resumesService.createResume(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
      setShowCreateForm(false);
      setNewResumeTitle('');
      setNewResumeContent('');
    },
  });

  const setPrimaryMutation = useMutation({
    mutationFn: (resumeId: string) => resumesService.setPrimaryResume(resumeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
    },
  });

  const deleteResumeMutation = useMutation({
    mutationFn: (resumeId: string) => resumesService.deleteResume(resumeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] });
    },
  });

  const analyzeResumeMutation = useMutation({
    mutationFn: (data: ResumeAnalysisRequest) => aiService.analyzeResume(data),
    onSuccess: (data) => {
      alert(`ATS Score: ${data.ats_score}/100\n\nImprovements:\n${data.improvements.join('\n')}`);
    },
  });

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    createResumeMutation.mutate({
      title: newResumeTitle,
      content: newResumeContent,
      is_primary: false,
    });
  };

  const handleSetPrimary = (resumeId: string) => {
    setPrimaryMutation.mutate(resumeId);
  };

  const handleDelete = (resumeId: string) => {
    if (confirm('Are you sure you want to delete this resume?')) {
      deleteResumeMutation.mutate(resumeId);
    }
  };

  const handleAnalyze = (resume: ResumeResponse) => {
    analyzeResumeMutation.mutate({
      resume_content: resume.content,
      resume_id: resume.id,
    });
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link href="/dashboard">
              <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">CareerOS</h1>
            </Link>
            <Link href="/dashboard" className="text-sm text-gray-600 dark:text-gray-400 hover:underline">
              ← Back to Dashboard
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">My Resumes</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Create and manage your resumes with AI-powered optimization.
          </p>
        </div>

        {/* Create Button */}
        <div className="mb-6">
          <Button onClick={() => setShowCreateForm(!showCreateForm)}>
            {showCreateForm ? 'Cancel' : '+ Create New Resume'}
          </Button>
        </div>

        {/* Create Form */}
        {showCreateForm && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Create New Resume</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreate} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium mb-1">
                    Title
                  </label>
                  <Input
                    id="title"
                    placeholder="e.g., Software Engineer Resume"
                    value={newResumeTitle}
                    onChange={(e) => setNewResumeTitle(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="content" className="block text-sm font-medium mb-1">
                    Content
                  </label>
                  <textarea
                    id="content"
                    rows={8}
                    className="w-full px-3 py-2 border rounded-md dark:bg-gray-800 dark:border-gray-700"
                    placeholder="Paste your resume content here..."
                    value={newResumeContent}
                    onChange={(e) => setNewResumeContent(e.target.value)}
                    required
                  />
                </div>
                <Button type="submit" disabled={createResumeMutation.isPending}>
                  {createResumeMutation.isPending ? 'Creating...' : 'Create Resume'}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Resumes List */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : resumes.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                No resumes yet. Create your first resume to get started!
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {resumes.map((resume: ResumeResponse) => (
              <Card key={resume.id} className={resume.is_primary ? 'border-blue-500 border-2' : ''}>
                <CardContent className="pt-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {resume.title}
                        </h3>
                        {resume.is_primary && (
                          <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded">
                            Primary
                          </span>
                        )}
                        {resume.ats_score !== undefined && (
                          <span className="px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded">
                            ATS: {resume.ats_score}/100
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                        Updated: {new Date(resume.updated_at).toLocaleDateString()}
                      </p>
                      <p className="text-gray-600 dark:text-gray-400 mt-2 line-clamp-2">
                        {resume.content.slice(0, 200)}...
                      </p>
                    </div>
                    <div className="flex flex-col gap-2 ml-4">
                      {!resume.is_primary && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleSetPrimary(resume.id)}
                          disabled={setPrimaryMutation.isPending}
                        >
                          Set as Primary
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleAnalyze(resume)}
                        disabled={analyzeResumeMutation.isPending}
                      >
                        Analyze
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(resume.id)}
                        disabled={deleteResumeMutation.isPending}
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
