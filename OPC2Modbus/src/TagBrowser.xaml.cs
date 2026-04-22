using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using OPCAutomation;

namespace OPC2Modbus
{
    public partial class TagBrowser : Window
    {
        private OPCServer opcServer;
        public List<string> SelectedTags { get; private set; }

        public TagBrowser(OPCServer server)
        {
            InitializeComponent();
            opcServer = server;
            SelectedTags = new List<string>();
            LoadOPCTags();
        }

        private void LoadOPCTags()
        {
            try
            {
                var rootNode = new TagNode { Name = "Root" };
                BrowseOPCTags(opcServer.OPCBrowseServerAddressSpace(OPCDataSource.OPCDevice), rootNode);
                tvTags.Items.Add(rootNode);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error browsing tags: " + ex.Message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void BrowseOPCTags(OPCBrowser browser, TagNode parentNode)
        {
            try
            {
                browser.ShowBranches();
                foreach (var branch in (Array)browser.Branches)
                {
                    var branchNode = new TagNode { Name = branch.ToString(), Parent = parentNode };
                    parentNode.Children.Add(branchNode);
                    browser.MoveDown(branch.ToString());
                    BrowseOPCTags(browser, branchNode);
                    browser.MoveUp();
                }

                browser.ShowLeafs();
                foreach (var leaf in (Array)browser.Leafs)
                {
                    var leafNode = new TagNode { Name = leaf.ToString(), IsLeaf = true, Parent = parentNode };
                    parentNode.Children.Add(leafNode);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error browsing tags: " + ex.Message);
            }
        }

        private void btnSelect_Click(object sender, RoutedEventArgs e)
        {
            // Get selected tags
            foreach (var item in tvTags.SelectedItems)
            {
                var node = item as TagNode;
                if (node != null && node.IsLeaf)
                {
                    // Build full tag path
                    string tagPath = node.Name;
                    var parent = node.Parent;
                    while (parent != null && parent.Name != "Root")
                    {
                        tagPath = parent.Name + "." + tagPath;
                        parent = parent.Parent;
                    }
                    SelectedTags.Add(tagPath);
                }
            }
            DialogResult = true;
            Close();
        }

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }

    public class TagNode
    {
        public string Name { get; set; }
        public List<TagNode> Children { get; set; }
        public TagNode Parent { get; set; }
        public bool IsLeaf { get; set; }

        public TagNode()
        {
            Children = new List<TagNode>();
            IsLeaf = false;
        }
    }
}