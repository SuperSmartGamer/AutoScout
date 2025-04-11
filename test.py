import os, cv2, csv, tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# 1) choose directory
root = tk.Tk(); root.withdraw()
video_dir = filedialog.askdirectory(title="Select video directory")
if not video_dir: raise SystemExit("No directory selected")  # cancel

# 2) frame‐skip interval
skip = int(input("Enter frame skip (every X frames): "))

# 3) prepare CSV
out_csv = os.path.join(video_dir, "labels.csv")
csvf = open(out_csv, "w", newline="", encoding="utf-8")
writer = csv.writer(csvf)
writer.writerow(["video_file","frame_no","robots","coral","algae",
                 "reef","barge","cages","net","processor","other"])

class Labeler:
    def __init__(self, master, vids):
        self.master, self.vids = master, vids
        self.v_idx = 0; self.cap = None; self.frame_no = 0
        self.setup_ui(); self.load_video()

    def setup_ui(self):
        self.canvas = tk.Label(self.master); self.canvas.pack()
        self.vars = {}
        for lbl in ["robots","coral","algae","reef","barge",
                    "cages","net","processor","other"]:
            v = tk.IntVar()
            tk.Checkbutton(self.master, text=lbl.capitalize(), variable=v).pack(side="left")
            self.vars[lbl] = v
        tk.Button(self.master, text="Next", command=self.next_frame).pack(side="bottom")

    def load_video(self):
        if self.cap: self.cap.release()
        if self.v_idx >= len(self.vids):
            print("Done"); self.master.quit(); return
        self.cap = cv2.VideoCapture(self.vids[self.v_idx]); self.frame_no = 0
        self.next_frame()

    def next_frame(self):
        # record last labels
        if hasattr(self, "current"):
            row = [self.current, self.frame_no]
            for lbl,v in self.vars.items():
                row.append(v.get()); v.set(0)
            writer.writerow(row); csvf.flush()
        # find next valid frame
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.v_idx += 1; self.load_video(); return
            self.frame_no += 1
            if self.frame_no % skip == 0: break
        self.current = os.path.basename(self.vids[self.v_idx])
        # display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.canvas.imgtk = img; self.canvas.config(image=img)

if __name__ == "__main__":
    vids = [os.path.join(video_dir,f) for f in os.listdir(video_dir)
            if f.lower().endswith((".mp4",".avi"))]
    root = tk.Tk()
    Labeler(root, vids)
    root.mainloop()
    csvf.close()
    print(f"Saved labels to {out_csv}")
